import re


def print_stat(file, num_msgs, num_occurr, dict_vocab_ocurr):
    file.write("Numero de mensagens: {:,}".format(num_msgs) + "\n")
    file.write("Número de occorrencias: {:,}".format(num_occurr) + "\n")
    file.write("Tamanho do vocabulário: {:,}".format(len(dict_vocab_ocurr.keys())) + "\n")


re_palavra = re.compile(r'[a-zA-Z_-]+')
re_hashtag_palavra = re.compile(r'#[a-zA-Z_-]+')
re_digitos_com_ponto_traco = re.compile(r'[0-9\.,/-]+')
re_email = re.compile(r'[^@]+@[^.]+\..+')


def type_word_count(file,arrWords):
    arr_palavras = []
    c_palavras = 0
    c_digitos = 0
    c_email = 0
    c_hashtag_palavra = 0
    c_outros = 0
    digitos_pt = []
    outros = []
    for word in arrWords:
        if(re_palavra.fullmatch(word)):
            c_palavras += 1
            if(c_palavras <= 10):
                arr_palavras.append(word)
        elif(re_hashtag_palavra.fullmatch(word)):
            c_hashtag_palavra += 1
        elif(re_digitos_com_ponto_traco.fullmatch(word)):
            c_digitos += 1
            digitos_pt += [word]
        elif(re_email.fullmatch(word)):
            c_email += 1
        else:
            outros += [word]
            c_outros += 1
    file.write("\tPalavras: {:,} {}".format(c_palavras, str(arr_palavras)) + "\n")
    file.write("\tPalavras (com hashtag): {:,}".format(c_hashtag_palavra) + "\n")
    file.write("\tDigitos com ponto e traços: {:,}".format(c_digitos) + "\n")
    file.write("\tEmails: {:,}".format(c_email) + "\n")
    file.write("\tOutros: {:,}".format(c_outros) + "\n")
    file.write("\n=== OUTROS ===\n")
    file.write("\n".join([str(x) for x in outros]))
    file.write("\n=== Digitos com ponto e traços ===\n")
    file.write("\n".join([str(x) for x in digitos_pt]))
    return c_palavras
