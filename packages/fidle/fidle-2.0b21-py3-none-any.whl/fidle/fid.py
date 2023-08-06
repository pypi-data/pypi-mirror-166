
# ------------------------------------------------------------------
#   ______ _     _ _                    _           _       
#  |  ____(_)   | | |          /\      | |         (_)      
#  | |__   _  __| | | ___     /  \   __| |_ __ ___  _ _ __  
#  |  __| | |/ _` | |/ _ \   / /\ \ / _` | '_ ` _ \| | '_ \ 
#  | |    | | (_| | |  __/  / ____ \ (_| | | | | | | | | | |
#  |_|    |_|\__,_|_|\___| /_/    \_\__,_|_| |_| |_|_|_| |_|
#                                                  Fidle admin (fid)
# ------------------------------------------------------------------
# A simple class to admin fidle bizness : fid command
# Jean-Luc Parouty CNRS/MIAI/SIMaP 2022


from asyncio import format_helpers
from genericpath import isdir
import os
import sys
import argparse
from typing_extensions import Required
import yaml
import importlib

import fidle.config as config
import fidle.utils  as utils
from fidle.Chrono      import Chrono
from fidle.TocBuilder  import TocBuilder
from fidle.MagicCooker import MagicCooker
from fidle.Installer   import Installer


__version__        = config.VERSION
use_interactivity  = False                # by default


# ------------------------------------------------------------------
# -- Check
# ------------------------------------------------------------------
#
def do_check(args):
    '''
    Check Fidle environment.
    '''
    print('Check environment : \n')
    # ---- Check datasets
    #
    version = None
    try:
        # Get env var
        datasets_dir = os.environ['FIDLE_DATASETS_DIR']
        # Get about file
        with open(f'{datasets_dir}/about.yml') as file:
            about = yaml.full_load(file)
        # Get version
        version   = about['version']
        print(f'    Fidle datasets       : Ok         ({version})')

    except Exception as e:
        print(f'    Fidle datasets       : **WRONG**')
        print('\n    *** Datasets cannot be found !')
        print('    *** Possible reasons are:')
        print('    ***     - the environment variable FIDLE_DATASET_DIR is not defined')
        print('    ***     - the path specified by the variable is incorrect')
        print('    ***     - the datasets directory is a too old version')
        print('    *** See documentation : https://fidle.cnrs.fr/installation\n')

    # ---- Check fidle-mod
    #
    print(f'    Fidle module         : Ok         ({config.VERSION})')

    for mod in config.USED_MODULES:
        try:
            importlib.import_module(mod)
            print(f'    {mod:21s}: Ok         ({sys.modules[mod].__version__})')
        except:
            print(f'    {mod:21s}: Not found')
    print('')


# ------------------------------------------------------------------
# -- Toc
# ------------------------------------------------------------------
#
def do_toc(args):
        print('Update TOC in readme : \n')
        tb       = TocBuilder()
        tb.update( about_file = args.about_file, 
                   root_dir   = args.root_dir )

# ------------------------------------------------------------------
# -- reset_ci
# ------------------------------------------------------------------
#
def do_reset_ci(args):
        print('Reset continous intégration campain : \n')
        if not are_you_sure(args.quiet) : return
        mck = MagicCooker()
        mck.reset_campain( args.profile,
                           root_dir    =  args.root_dir,
                           filters     =  args.filter, 
                           campain_tag =  args.campain_tag)

# ------------------------------------------------------------------
# -- run_ci
# ------------------------------------------------------------------
#
def do_run_ci(args):
        print('Run continous intégration campain : \n')
        if not are_you_sure(args.quiet) : return
        mck = MagicCooker()
        mck.run_campain( args.profile,
                         root_dir    =  args.root_dir,
                         filters     =  args.filter, 
                         campain_tag =  args.campain_tag)


# ------------------------------------------------------------------
# -- install
# ------------------------------------------------------------------
#
def do_install(args):
        install_dir = os.path.expanduser(args.install_dir)

        print(f'This will install all notebooks and datasets in : {install_dir}\n')

        # ---- Check if exist / empty
        #
        if os.path.isdir(install_dir):
            if len(os.listdir(install_dir))>0:
                print(f'*** Oups, installation directory ({install_dir}) already exist and is not empty...')
                print('*** You can clean it or specify another directory with the option --install_dir <path>\n')
                return
        else:
            utils.mkdir(install_dir)
            print('Directory created.\n')

        # ---- Install
        #
        installer=Installer()
 
        print(f'Install Fidle notebooks in {args.install_dir} : \n')
        if not are_you_sure(args.quiet) : return
        installer.install_ressource( catalog_name     = 'notebooks', 
                                     ressource_name   = args.notebooks, 
                                     installation_dir = args.install_dir )

        print(f'Install Fidle datasets in  {args.install_dir} : \n')
        if not are_you_sure(args.quiet) : return
        installer.install_ressource( catalog_name     = 'datasets', 
                                     ressource_name   = args.datasets, 
                                     installation_dir = args.install_dir )



# ------------------------------------------------------------------
# -- install notebooks
# ------------------------------------------------------------------
#
def do_install_notebooks(args):
        print(f'Install Fidle notebooks in {args.notebooks_dir} : \n')
        if not are_you_sure(args.quiet) : return
        installer=Installer()
        installer.install_ressource( catalog_name     = 'notebooks', 
                                     ressource_name   = args.notebooks, 
                                     installation_dir = args.notebooks_dir )

# ------------------------------------------------------------------
# -- install datasets
# ------------------------------------------------------------------
#
def do_install_datasets(args):
        print(f'Install Fidle datasets in {args.datasets_dir} : \n')
        if not are_you_sure(args.quiet) : return
        installer=Installer()
        installer.install_ressource( catalog_name     = 'datasets', 
                                     ressource_name   = args.datasets, 
                                     installation_dir = args.datasets_dir )

# ------------------------------------------------------------------
# -- show_resources
# ------------------------------------------------------------------
#
def do_show_ressources(args):
        installer=Installer()
        installer.show_catalog('notebooks')
        installer.show_catalog('datasets')


# ------------------------------------------------------------------
# -- Are you sure ?
# ------------------------------------------------------------------
#
def are_you_sure(quiet):
        if quiet :                return True
        if not use_interactivity: return True
        print('\nAre you sure ? (Y/N) ', end='')
        rep=input()
        print('')
        return (rep=='Y')


# ------------------------------------------------------------------
# Run / Module method
# ------------------------------------------------------------------
#
# Run a command, directly from python : fidle.admin.run( )
# Or via an entry point / command line
#
def run(*arguments):
    print('\n==========================================================')
    print(f'fid - Your favorite Fidle admin command :-)    (v{config.VERSION})')
    print('==========================================================\n')

    usage='''
    fid

      check                                   Check environment

      install                                 Install notebooks and datasets
            [--notebooks   <ress. name> ]        Notebooks ressource name      (default)
            [--datasets    <ress. name> ]        Datasets ressource name       (default)
            [--install_dir <directory>  ]        The place to install          (./fidle-tp)
            [--quiet                    ]        Quiet mode

      install_notebooks                       Install notebooks
            [--notebooks   <ress. name> ]        Notebooks ressource name      (default)
            [--notebooks_dir <directory>]        The place to install          (.)
            [--quiet                    ]        Quiet mode

      install_datasets                        Install datasets
            [--datasets    <ress. name> ]        Datasets ressource name       (default)
            [--datasets_dir <directory> ]        The place to install          (.)
            [--quiet                    ]        Quiet mode

      show_ressources                         Show catalog of available ressources   

      toc                                     (re)Build readme.md and readme.ipynb
            [--about_file  <about file>]         About file                    (./fidle/about.yml)
            [--root_dir    <root dir>  ]         root dir of the notebooks     (.)

      run_ci                                   Run a continous integration campain
            [--root_dir    <root dir> ]          Root directory                (.)
            [--profile     <profile>  ]          Profile name                  (./fidle/ci/run-01.yml)
            [--filter      <filter>   ]          Filter to apply               (.*)
            [--campain_tag <tag>      ]          Campain tag                   (None)
            [--quiet                  ]          Quiet mode                

      reset_ci                                 Reset a continous integration campain
            [--root_dir    <root dir> ]          Root directory                (.)
            [--profile     <profile>  ]          Profile name                  (./fidle/ci/run-01.yml)
            [--filter      <filter>   ]          Filter to apply               (.*)
            [--campain_tag <tag>      ]          Campain tag                   (None)
            [--quiet                  ]          Quiet mode
      
      help | --help                            Help             
    '''

    # ---- Parser
    #
    parser = argparse.ArgumentParser( exit_on_error=True,
                                      description="Fidle admin command (fid)",
                                      usage=usage)

    parser.add_argument('cmd',               help=argparse.SUPPRESS,    default='help')
                 
    parser.add_argument('--notebooks',             dest='notebooks',          help=argparse.SUPPRESS,    default='default')
    parser.add_argument('--datasets',              dest='datasets',           help=argparse.SUPPRESS,    default='default')
    parser.add_argument('--install_dir',           dest='install_dir',        help=argparse.SUPPRESS,    default='./fidle-tp')
    parser.add_argument('--notebooks_dir',         dest='notebooks_dir',      help=argparse.SUPPRESS,    default='.')
    parser.add_argument('--datasets_dir',          dest='datasets_dir',       help=argparse.SUPPRESS,    default='.')
    parser.add_argument('--root_dir',              dest='root_dir',           help=argparse.SUPPRESS,    default='.')
    parser.add_argument('--about_file',            dest='about_file',         help=argparse.SUPPRESS,    default='./fidle/about.yml')
    parser.add_argument('--profile',               dest='profile',            help=argparse.SUPPRESS,    default='./fidle/ci/run-01.yml')
    parser.add_argument('--filter',                dest='filter',             help=argparse.SUPPRESS,    default='.*')
    parser.add_argument('--campain_tag',           dest='campain_tag',        help=argparse.SUPPRESS,    default=None)
    parser.add_argument('--quiet',                 dest='quiet',              help=argparse.SUPPRESS,    action='store_true')
    
    try:
        args  = parser.parse_args(arguments)
    except:
        print('\n')
        return

    # ---- Command
    #
    if   args.cmd=='check'                :  do_check(args)
    elif args.cmd=='install'              :  do_install(args)
    elif args.cmd=='install_notebooks'    :  do_install_notebooks(args)
    elif args.cmd=='install_datasets '    :  do_install_datasets(args)
    elif args.cmd=='show_ressources'      :  do_show_ressources(args)
    elif args.cmd=='toc'                  :  do_toc(args)
    elif args.cmd=='reset_ci'             :  do_reset_ci(args)
    elif args.cmd=='run_ci'               :  do_run_ci(args)
    else: print(usage)    


# ------------------------------------------------------------------
# Run / Pypi entry point
# ------------------------------------------------------------------
# fidle.admin --help
#
def main():
    global use_interactivity
    
    # ---- We are in command line mode
    use_interactivity = True

    run(*sys.argv[1:])    


# ------------------------------------------------------------------
# Run / Command line
# ------------------------------------------------------------------
# python -m fidle.admin --help
#
if __name__ == '__main__':

    # ---- We are in command line mode
    use_interactivity = True

    run(*sys.argv[1:])    
