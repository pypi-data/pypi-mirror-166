#imports
import time
from abc import ABC, abstractmethod
from ..running.controlled_process_multi_threaded import ControlledProcessMultiThreaded
from .consumer_group import ConsumerGroup

class ControlledMessageProcessor(ControlledProcessMultiThreaded,ConsumerGroup,ABC) :
    """
    Combine a ControlledProcessMultiThreaded and a ConsumerGroup to create a 
    single interface for reading and processing individual messages
    """

    CONSUMER_POLL_TIMEOUT = 0.050
    NO_MESSAGE_WAIT = 0.005 #how long to wait if consumer.get_next_message_value returns None

    def __init__(self,*args,**kwargs) :
        """
        Hang onto the number of messages read and processed
        """
        self.n_msgs_read = 0
        self.n_msgs_processed = 0
        super().__init__(*args,**kwargs)
        self.restart_at_beginning = False #set to true to reset new consumers to their earliest offsets
        self.message_key_regex = None #set to some regex to filter messages by their keys
        self.filter_new_messages = False #reset the regex after the consumer has filtered through previous messages

    def _run_worker(self):
        """
        Handle startup and shutdown of a thread-independent Consumer and 
        serve individual messages to the _process_message function
        """
        #create the Consumer for this thread
        if self.alive :
            consumer = self.get_new_subscribed_consumer(restart_at_beginning=self.restart_at_beginning,
                                                        message_key_regex=self.message_key_regex,
                                                        filter_new_messages=self.filter_new_messages)
        if ('enable.auto.commit' not in consumer.configs.keys()) or (consumer.configs['enable.auto.commit'] is True) :
            warnmsg = 'WARNING: enable.auto.commit has not been set to False for a Consumer that will manually commit '
            warnmsg+= 'offsets. Missed or duplicate messages could result. You can set "enable.auto.commit"=False in '
            warnmsg+= 'the "consumer" section of the config file to re-enable manual offset commits (recommended).'
            self.logger.warning(warnmsg)
        #start the loop for while the controlled process is alive
        last_message = None
        while self.alive :
            #consume a message from the topic
            msg = consumer.get_next_message(ControlledMessageProcessor.CONSUMER_POLL_TIMEOUT)
            if msg is None :
                time.sleep(ControlledMessageProcessor.NO_MESSAGE_WAIT) #wait just a bit to not over-tax things
                continue
            with self.lock :
                self.n_msgs_read+=1
            last_message = msg
            #send the message to the _process_message function
            retval = self._process_message(self.lock,msg)
            #count and (asynchronously) commit the message as processed (if it wasn't consumed already in the past)
            if retval :
                with self.lock :
                    self.n_msgs_processed+=1
                if not consumer._message_consumed_before(msg) :
                    tps = consumer.commit(msg)
                    if tps is not None :
                        for tp in tps :
                            if tp.error is not None :
                                warnmsg = 'WARNING: failed to synchronously commit offset of last message received on '
                                warnmsg+= f'"{tp.topic}" partition {tp.partition}. Duplicate messages may result when this '
                                warnmsg+= f'Consumer is restarted. Error reason: {tp.error.str()}'
                                self.logger.warning(warnmsg)
        #commit the offset of the last message received if it wasn't already consumed in the past (block until done)
        if (last_message is not None) and (not consumer._message_consumed_before(last_message)) :
            try :
                tps = consumer.commit(last_message,asynchronous=False)
                if tps is not None :
                    for tp in tps :
                        if tp.error is not None :
                            warnmsg = 'WARNING: failed to synchronously commit offset of last message received on '
                            warnmsg+= f'"{tp.topic}" partition {tp.partition}. Duplicate messages may result when this '
                            warnmsg+= f'Consumer is restarted. Error reason: {tp.error.str()}'
                            self.logger.warning(warnmsg)
            except Exception as e :
                errmsg = 'WARNING: failed to synchronously commit offset of last message received. '
                errmsg+= 'Duplicate messages may be read the next time this Consumer is started. '
                errmsg+= 'Error will be logged below but not re-raised.'
                self.logger.error(errmsg,exc_obj=e,reraise=False)
        #shut down the Consumer that was created once the process isn't alive anymore
        consumer.close()

    def _on_shutdown(self):
        super()._on_shutdown()
        self.close()

    @abstractmethod
    def _process_message(self,lock,msg,*args,**kwargs) :
        """
        Process a single message read from the thread-independent Consumer
        Returns true if processing was successful, and False otherwise
        
        lock = lock across all created child threads (use to enforce thread safety during processing)
        msg  = a single message that was consumed and should be processed by this function

        Not implemented in the base class 
        """
        raise NotImplementedError
