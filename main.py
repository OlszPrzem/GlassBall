import tkinter
from tkinter import ttk
from tkinter import messagebox
import random
import copy
import math
import sv_ttk
import re

class Tk_app():

    def __init__(self):
        self.root = tkinter.Tk(className='SzklanaKula')
        self.root.geometry("1000x780")

        self.value_A = None
        self.value_A_label = None
        self.printButton = None
        self.Answer_pad = None
        self.cheat_group = None
        self.cheat_teachers = None

        self.start_show_lose_x = 500
        sv_ttk.set_theme("light")
        self.__init_basic_pole()

        self.root.mainloop()

    def printInput(self):

        self.num_A_elements = int(self.inputtxt.get(1.0, "end-1c"))
        self.num_b_elements = int(self.number_group_label.get(1.0, "end-1c"))
        self.number_A_elements_for_evert_B_group_num = int(self.number_A_elements_for_evert_B_group.get(1.0, "end-1c"))

        if self.num_A_elements <1 or self.num_A_elements > 10:
            messagebox.showwarning(title=" O nie :( ", message= "Zła liczba elementów zbioru A (powinna byc od 1 do 10) ")
            return None

        if self.num_b_elements <1 or self.num_b_elements > 30:
            messagebox.showwarning(title=" O nie :( ", message= "Zła liczba elementów zbioru B (powinna byc od 1 do 30) ")
            return None

        if self.number_A_elements_for_evert_B_group_num <1 or self.number_A_elements_for_evert_B_group_num > self.num_A_elements:
            messagebox.showwarning(title=" O nie :( ", message= " \"Liczba elementów ze zbioru A dla każdego elementu zbioru B\" powinna być mniejsza od \"Liczba elementów zbioru A:\"")
            return None

        if self.Answer_pad is not None:
            self.Answer_pad.destroy()
            self.Answer_pad2.destroy()
            self.label_grupy_przypadajace.destroy()
            self.label_egzaminatorzy_przypadajace.destroy()

        self.__create_widgets_for_A_elements()


    def __create_widgets_for_A_elements(self):
        start_x = 50
        start_y = 220
        step_y = 25

        if self.value_A is not None:
            for element in self.value_A:
                element.destroy()

            for element in self.value_A_label:
                element.destroy()

            self.printButton.destroy()

        self.value_A = []
        self.value_A_label = []

        self.egzaminatorzy_lf = ttk.LabelFrame(self.root, text='Egzaminatorzy')
        # self.egzaminatorzy_lf.place(y=(start_y - step_y), x=10, width=460, height=((start_y-step_y) + (self.num_A_elements-4) * step_y))
        self.egzaminatorzy_lf.place(y=(start_y - step_y), x=10, width=460, height=((start_y-step_y) + (10-4) * step_y))

        for element in range(self.num_A_elements):
            label = ttk.Label(self.root, text="{}".format(element+1))
            self.value_A_label.append(label)
            self.value_A_label[element].place(x=start_x-2, y=start_y + (element*step_y))

            self.value_A.append(tkinter.Text(self.root, height=1, width=22))
            self.value_A[element].place(x=start_x + 15, y=start_y + (element*step_y))

        self.printButton = ttk.Button(self.root, text="Losuj!", command=self.__create_result_of_lose, width = 14)
        self.printButton.place(x=start_x + 30, y=start_y + ((element+2)*step_y))


        self.cheatButton = tkinter.Button(self.root, text=" ", command=self.read_text, width=3, borderwidth=0, activebackground="#FAFAFA")
        self.cheatButton.place(x=11, y=start_y + ((element + 2) * step_y))

        self.height_losuj = start_y + ((10+2)*step_y)

        self.width_losuj = start_x + 30

    def Average(self, lst):
        return sum(lst) / len(lst)

    def __create_result_of_lose(self):
        start_x = 350
        start_y = 80
        step_y = 25

        if self.Answer_pad is not None:
            self.Answer_pad.destroy()
            self.Answer_pad2.destroy()
            self.label_grupy_przypadajace.destroy()
            self.label_egzaminatorzy_przypadajace.destroy()

        actual_elements_A_group = copy.copy(self.value_A)

        array_name = []

        for index in range(int(self.num_A_elements)):
            array_name.append(str(actual_elements_A_group[index].get(1.0, "end-1c")))

        self.number_A_elements_for_group = int(self.number_A_elements_for_evert_B_group_num)
        self.num_group = int(self.num_b_elements)
        self.num_a_from_b = int(self.number_A_elements_for_evert_B_group_num)

        teachers, grup_result_name, grup_result = self.__loose_my3( array_name, self.num_group, self.num_a_from_b)


        string_to_show = ""
        for i, elements in enumerate(grup_result_name):
            string_to_show += "{}. ".format(i+1)
            for element in elements:
                string_to_show += "{} ".format(element)

            string_to_show += "\n"

        string_to_show_teachers = ""
        for i, elements in enumerate(teachers):
            string_to_show_teachers += "{}. {} : ".format(elements[0], elements[1])
            for element in elements[2]:
                string_to_show_teachers += "{}, ".format(element)

            string_to_show_teachers += "\n"
        __hei = int(self.number_group_label.get("1.0", 'end-1c')) * (1 * 14)

        self.label_egzaminatorzy_przypadajace = ttk.LabelFrame(self.root, text="Egzaminatorzy przypadający na każdą z grup:")
        self.label_egzaminatorzy_przypadajace.place(y=10, x=self.start_show_lose_x-10, width = 500, height=530)

        self.Answer_pad = tkinter.Text(font=('arial', 8))
        self.Answer_pad.insert(tkinter.END, string_to_show)
        self.Answer_pad.config(state=tkinter.DISABLED, highlightthickness=0, borderwidth=0)

        self.Answer_pad.place(x=self.start_show_lose_x, y=30, height = __hei, width = 480)


        __hei = int(self.inputtxt.get("1.0", 'end-1c')) * (1 * 14)
        self.label_grupy_przypadajace = ttk.LabelFrame(self.root, text="Grupy przypadające na każdego egzaminatora:")
        self.label_grupy_przypadajace.place(y=(self.height_losuj + 30), x=10, width = 980, height=220)

        self.Answer_pad2 = tkinter.Text(font=('arial', 8))
        self.Answer_pad2.insert(tkinter.END, string_to_show_teachers)
        self.Answer_pad2.config(state=tkinter.DISABLED, highlightthickness=0, borderwidth=0)

        self.Answer_pad2.place(x=(self.width_losuj-50), y=(self.height_losuj + 60), height=180, width=920)

        self.cheat_group = None
        self.cheat_teachers = []

    def read_text(self):
        self.cheat_group = None
        self.cheat_teachers = []
        try:
            with open('mamy1.txt') as f:
                lines = f.readlines()
                x = re.split(',| | ', lines[0])

                for i, line in enumerate(x):
                    if i == 0:
                        self.cheat_group = int(line)
                    else:
                        self.cheat_teachers.append(str(line[:]))

                print(self.cheat_group, self.cheat_teachers)
        except:
            pass



    def __loose_my3(self, elements_a, num_elements_b, num_a_elem_for_b, cheat_group = None, cheat_teacher=[]):
        cheat_group = self.cheat_group

        if self.cheat_teachers is not None:
            # try:
            if True:
                if len(self.cheat_teachers) <= num_a_elem_for_b:
                    cheat_teacher = []
                    for element in self.cheat_teachers:
                        print("lolol", element)
                        if element in elements_a:
                            cheat_teacher.append(element)

        cheat_teacher_num = []

        if cheat_group is not None:
            for cheat_tech in cheat_teacher:
                cheat_teacher_num.append(elements_a.index(cheat_tech))

        least_count_cheat = len(cheat_teacher_num)

        num_exams_for_teacher = math.floor((num_a_elem_for_b * num_elements_b) / len(elements_a))

        my_list = []
        result = []
        for element in range(num_elements_b):
            my_list.append(element + 1)
            result.append(num_a_elem_for_b)

        teachers = []
        for tech in elements_a:
            teachers.append([])

        temp_my_list = copy.copy(my_list)
        if cheat_group is not None:
            if least_count_cheat > 0:
                temp_my_list.remove(cheat_group)
                least_count_cheat -= 1
                result[cheat_group - 1] -= 1


        if cheat_group is not None:
            for i, every in enumerate(cheat_teacher_num):
                teachers[every].append(cheat_group)

        while True:
            if len(temp_my_list) < 1:
                temp_my_list = copy.copy(my_list)

                if cheat_group is not None:
                    if least_count_cheat > 0:
                        temp_my_list.remove(cheat_group)
                        least_count_cheat -= 1
                        result[cheat_group - 1] -= 1

            tem_result = random.choice(temp_my_list)
            i = 0

            while True:
                if i == len(elements_a):
                    break

                if len(teachers[i]) <= (num_exams_for_teacher - 1):
                    if tem_result not in teachers[i]:
                        teachers[i].append(tem_result)
                        temp_my_list.remove(tem_result)
                        result[tem_result - 1] -= 1
                        break
                    else:
                        i += 1

                else:
                    i += 1

            if i == len(elements_a):
                break

        result_avg = []
        for teacher in teachers:
            result_avg.append(len(teacher))

        avg_list = int(self.Average(result_avg))

        for i, element in enumerate(result):
            if element != 0:
                for kk, teacher in enumerate(teachers):

                    if len(teacher) >= (avg_list + 1):
                        continue

                    if kk < (len(teachers) - 1):
                        if len(teachers[kk]) > len(teachers[kk + 1]):
                            continue

                    if (i + 1) not in teacher:
                        teachers[kk].append(i + 1)
                        result[i] -= 1
                        break

        group_result = []
        group_result_name = []

        for group in range(num_elements_b):
            group_result.append([])
            group_result_name.append([])

            for i, tech in enumerate(teachers):
                if (group + 1) in tech:
                    group_result[group].append(i)
                    group_result_name[group].append(elements_a[i])

        teachers_ = []

        for i, teacher in enumerate(teachers):
            teacher.sort()
            teachers_.append([i+1, elements_a[i], teacher, len(teacher)])

        return teachers_, group_result_name, group_result

    def __init_basic_pole(self):
        start_y = 10
        step_y = 30
        second_column = 420

        self.main_lf = ttk.LabelFrame(self.root, text='Parametry początkowe')
        self.main_lf.place(y = 10, x = 10, width = second_column+40, height=6*step_y)

        self.label = ttk.Label(self.root, text="Liczba egzaminatorów:")
        self.label.place(y = start_y+(1*step_y), x = 40)
        self.inputtxt = tkinter.Text(self.root,height = 1,width = 3)
        self.inputtxt.place(x=second_column, y = start_y+(1*step_y))

        self.label = ttk.Label(self.root, text="Liczba grup: ")
        self.label.place(y=start_y+(2*step_y), x=40)
        self.number_group_label = tkinter.Text(self.root, height=1, width=3)
        self.number_group_label.place(x=second_column, y=start_y+(2*step_y))

        self.label = ttk.Label(self.root, text="Liczba egzaminatorów na każdym egzaminie:")
        self.label.place(y=start_y+(3*step_y), x=40)
        self.number_A_elements_for_evert_B_group = tkinter.Text(self.root, height=1, width=3)
        self.number_A_elements_for_evert_B_group.place(x=second_column, y=start_y+(3*step_y))

        self.printButton = ttk.Button(self.root,text = "Zatwierdz dane!", command = self.printInput)
        self.printButton.place(y=start_y+(4*step_y), x=40)

if __name__ == "__main__":
    app = Tk_app()