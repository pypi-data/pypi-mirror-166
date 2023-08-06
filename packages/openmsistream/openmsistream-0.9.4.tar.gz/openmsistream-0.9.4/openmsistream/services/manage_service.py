#imports
from .config import SERVICE_CONST
from .utilities import get_os_name
from .service_manager_base import ServiceManagerBase
from .windows_service_manager import WindowsServiceManager
from .linux_service_manager import LinuxServiceManager

def main(given_args=None) :
    #get the arguments
    parser = ServiceManagerBase.get_argument_parser('manage')
    args = parser.parse_args() if given_args is None else parser.parse_args(given_args)
    #get the name of the OS and start the object
    operating_system = get_os_name()
    manager_args = [args.service_name]
    manager_kwargs = {'interactive':True if given_args is None else False,
                      'logger':SERVICE_CONST.LOGGER}
    managers_by_os_name = {'Windows':WindowsServiceManager,
                           'Linux':LinuxServiceManager,}
    manager_class = managers_by_os_name[operating_system]
    manager = manager_class(*manager_args,**manager_kwargs)
    #run some function based on the run mode
    manager.run_manage_command(args.run_mode,
                               remove_env_vars=args.remove_env_vars,
                               remove_install_args=args.remove_install_args,
                               remove_nssm=args.remove_nssm)

if __name__=='__main__' :
    main()