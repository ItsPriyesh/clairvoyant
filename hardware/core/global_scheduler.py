from multiprocessing import Queue
from audio_recorder import record_process
from data_processor import audio_process
import multiprocessing
from ml_processor import ml_process


if __name__ == '__main__':

    #define queues
    audio_q = Queue()
    ml_q = Queue()
    ml_init_q = Queue()

    #start ml task
    ml_task = multiprocessing.Process(target=ml_process, args = (ml_q,ml_init_q,))
    ml_task.start()
    #wait for it to load model
    while (ml_init_q.empty() == True):
        pass
    ml_init_q.get()
    print ("Done ml init")
    

    #start Recorder Task
    recorder_task = multiprocessing.Process(target=record_process, args=(audio_q,))
    recorder_task.start()

    #start Data Procesing Task
    data_task = multiprocessing.Process(target=audio_process, args=(audio_q,ml_q,))
    data_task.start()

