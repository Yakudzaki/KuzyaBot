import logging

#Инициация глобальных переменных
def init_glob(): 
    global spam_list

    spam_list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    print("[-] Глобальные переменные инициированы!")
    logging.info('Глобальные переменные инициированы!')

#Внесение изменений в переменные для счетчиков спамлимитов
def set_cor(user_cor_v, chat_cor_v, cor_v, user_cor_st, chat_cor_st, cor_st, user_cor_a, chat_cor_a, cor_a, user_cor_tx, chat_cor_tx, cor_tx, user_cor_ph, chat_cor_ph, cor_ph):
    global spam_list
    spam_list = [user_cor_v, chat_cor_v, cor_v, user_cor_st, chat_cor_st, cor_st, user_cor_a, chat_cor_a, cor_a, user_cor_tx, chat_cor_tx, cor_tx, user_cor_ph, chat_cor_ph, cor_ph]

#Получение значений переменных для счетчика спамлимитов
def get_cor():
    global spam_list
    return spam_list