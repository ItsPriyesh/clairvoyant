from multiprocessing import Queue
from audio_recorder import record_process
from data_processor import audio_process
import multiprocessing


if __name__ == '__main__':

    #define queues
    audio_q = Queue()

    #start Recorder Task
    recorder_task = multiprocessing.Process(target=record_process, args=(audio_q,))
    recorder_task.start()

    #start Data Procesing Task
    data_task = multiprocessing.Process(target=audio_process, args=(audio_q,))
    data_task.start()

