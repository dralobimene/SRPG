# logger_config.py
import logging


def configure_logger(name, logfile='application.log', filemode='w'):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Créer un gestionnaire de fichiers qui enregistre les messages
    # de journalisation (fh = filehandler).
    fh = logging.FileHandler(logfile, mode=filemode)
    fh.setLevel(logging.DEBUG)

    # Créer un formatteur pour formatter les messages de journalisation.
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)

    # Ajouter le gestionnaire au logger.
    logger.addHandler(fh)

    return logger
