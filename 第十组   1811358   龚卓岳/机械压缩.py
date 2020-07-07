import pandas as pd

def depress(string):
    filelist = [string]
    filelist2 = []
    for a_string in filelist:
        temp1 = a_string.strip('\n')
        temp2 = temp1.lstrip('\ufeff')
        temp3 = temp2.strip('\r')
        char_list = list(temp3)
        list1 = []
        list1.append(char_list[0])
        list2 = ['']
        del1 = []
        i = 0
        while (i < len(char_list)):
            i = i + 1
            if i == len(char_list):
                if list1 == list2:
                    m = len(list2)
                    for x in range(i - m, i):
                        del1.append(x)
            else:
                if char_list[i] == list1[0] and list2 == ['']:
                    list2[0] = char_list[i]
                elif char_list[i] != list1[0] and list2 == ['']:
                    list1.append(char_list[i])
                elif char_list[i] != list1[0] and list2 != ['']:
                    if list1 == list2 and len(list2) >= 2:
                        m = len(list2)
                        for x in range(i - m, i):
                            del1.append(x)
                        list1 = ['']
                        list2 = ['']
                        list1[0] = char_list[i]
                    else:
                        list2.append(char_list[i])
                elif char_list[i] == list1[0] and list2 != ['']:
                    if list1 == list2:
                        m = len(list2)
                        for x in range(i - m, i):
                            del1.append(x)
                        list2 = ['']
                        list2[0] = char_list[i]
                    else:
                        list1 = list2
                        list2 = ['']
                        list2[0] = char_list[i]
        a = sorted(del1)
        t = len(a) - 1
        while (t >= 0):
            del char_list[a[t]]
            t = t - 1
        str1 = ''.join(char_list)
        str2 = str1.strip()
        filelist2.append(str2)
    return filelist2

if __name__ == "__main__":
    comments=pd.read_csv('comments.csv',encoding='utf-8',header=None)
    comments=comments.set_index(0,drop=True)
    for i in range(len(comments.index)):
        comments.iloc[i][1]=(depress(comments.iloc[i][1])[0])
    comments.to_csv('comments.csv', encoding='utf-8', header=False)
