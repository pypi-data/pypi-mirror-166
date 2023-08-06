import pandas as pd
import random
import tkinter as tk
from tkinter import simpledialog
from tkinter import *
import datetime,os,time
import threading
from tkinter import filedialog
import threading
import ctypes
import time
try:
    from math_statistic import plot_math_statistics
except:
    from MathP.math_statistic import plot_math_statistics

class thread_with_exception(threading.Thread):
    def __init__(self, gui):
        threading.Thread.__init__(self)
        self.gui = gui
        # print(gui.font_s)

    def run(self):

        # target function of the thread class
        try:
            ts = int(self.gui.time_count)
            self.gui.Timer.configure(foreground="#000000")
            # while ts >= -0:
            while True:
                if self.gui.if_pause:
                    pass
                else:
                    self.gui.Timer.configure(text=ts)
                    ts-=1
                    # self.Timer.pack()
                    time.sleep(1)
                    if ts ==0:
                        # self.gui.Timer.config(text='''Time out''')
                        self.gui.Timer.configure(foreground="red")
        finally:
            print('ended')

    def get_id(self):

        # returns id of the respective thread
        if hasattr(self, '_thread_id'):
            return self._thread_id
        for id, thread in threading._active.items():
            if thread is self:
                return id

    def raise_exception(self):
        thread_id = self.get_id()
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id,
              ctypes.py_object(SystemExit))
        if res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
            print('Exception raise failure')

def get_val(para,res):
    try:
        return para.get()
    except:
        return res

def generate_problem_database():
    with open('math_source.csv','w') as f:
        f.write('Num1,operator,Num2,equal to,frequency,error times,correct times,right/n')


class math_practice():
    def __init__(self,data_file='math_source.csv'):
        try:
            self.df = pd.read_csv (data_file)
        except:
            generate_problem_database()
            self.df = pd.read_csv (data_file)
        # self.df = pd.DataFrame()
        self.df_backup = self.df.copy(deep=True)
        self.use_database = True
        self.problem_index = 0
        self.Problem_list = []
        self.right_list = []
        self.wrong_list = []
        self.outtime_list = []
        self.top_setting()
        self.create_widgets()
        self.report_dict = {}
        self.th = ''
        self.if_pause = False
        self.rounds_n = self.rounds_val.get()
        self.report_filename = ''

    def generate_new_folder(self,folder_name = "L_report"):
        # current_path = os.path.dirname(os.path.abspath(__file__))
        current_path = os.getcwd()
        if not os.path.isdir(os.path.join(current_path, folder_name)):
            os.mkdir(os.path.join(current_path, folder_name))
        return os.path.join(current_path, folder_name)

    def generate_report_file_path(self):
        self.report_filename = os.path.join(self.report_path,datetime.datetime.now().strftime('%Y%m%d_%H%M%S'))
        self.report_filename_htm = self.report_filename+'.htm'
        self.report_filename = self.report_filename+'.csv'

    def top_setting(self):
        self.top = Tk()
        self.top.geometry("800x500+521+201")
        self.top.minsize(120, 1)
        self.top.maxsize(1924, 1061)
        self.top.resizable(1, 1)
        self.top.title("New Toplevel")
        self.top.configure(background="#26f7d4")
        self.top.configure(highlightbackground="#26b467")
        self.top.configure(highlightcolor="#26f7d4")
        self.top.title('Math Practice')
        self.font_s = ('calibre',50,'normal')
        self.font_p = ('calibre',80,'normal')
        menu = Menu(self.top)
        self.top.config(menu=menu)
        fileMenu = Menu(menu)
        fileMenu.add_command(label="Generate", command=self.generate_problem_auto)
        fileMenu.add_command(label="Open",command=self.load)
        fileMenu.add_command(label="Exit", command=self.exitProgram)
        fileMenu.add_command(label="Analysis", command=self.analysis_callback)

        menu.add_cascade(label="File", menu=fileMenu)

    def generate_problem_auto(self):
        self.use_database=False
        self.get_parameters_for_auto_generate_problem()




    def get_parameters_for_auto_generate_problem(self):
        self.first_num_range_up_boundary = simpledialog.askinteger("Parameter input",
        'Input up boundary of first number range (Integer):',
        initialvalue='90',
        parent=self.top)

        self.first_num_range_down_boundary = simpledialog.askinteger("Parameter input",
        'Input down boundary of first number range (Integer):',
        initialvalue='0',
        parent=self.top)
        self.second_num_range_up_boundary = simpledialog.askinteger("Parameter input",
        'Input up boundary of second number range (Integer):',
        initialvalue='10',
        parent=self.top)
        self.second_num_range_down_boundary = simpledialog.askinteger("Parameter input",
        'Input down boundary of second number range (Integer):',
        initialvalue='6',
        parent=self.top)
        self.signs=second_num_range_down_boundary = simpledialog.askstring("Parameter input",
        'Input signs:',
        initialvalue='+,-,*',
        parent=self.top)
        self.signs = self.signs.split(',')

    def exitProgram(self):
        exit()
    def load(self):
        self.use_database=True
        self.load_txt()

    def analysis_callback(self):
        reportPath = filedialog.askdirectory(initialdir = os.getcwd())
        plot_math_statistics(folder = reportPath)

    def load_txt(self):
        input_text = []
        # os.getcwd()
        path_txt = filedialog.askopenfilename(title = "Select file",filetypes = (("CSV Files","*.csv"),))
        self.df = pd.read_csv (path_txt)
        self.df_backup = self.df.copy(deep=True)

    def create_widgets(self):
        self.Display_problem = tk.Label(self.top,font = self.font_p)
        # self.Display_problem.configure(font = self.font_s)
        self.Display_problem.place(relx=0.113, rely=0.4, height=80, width=400)
        self.Display_problem.configure(activebackground="#f9f9f9")
        self.Display_problem.configure(activeforeground="#26f7d4")
        self.Display_problem.configure(background="#26f7d4")
        self.Display_problem.configure(disabledforeground="#373737")
        self.Display_problem.configure(foreground="#000000")
        self.Display_problem.configure(highlightbackground="#26b467")
        self.Display_problem.configure(highlightcolor="#26f7d4")
        self.Display_problem.configure(text='''a+b=''')

        self.Answer_val = tk.IntVar()
        self.Answer = tk.Entry(self.top,font = self.font_p)
        self.Answer.configure(textvariable = self.Answer_val)
        # self.Answer.configure(font = self.font_s)
        self.Answer.place(relx=0.55, rely=0.4,height=80, width=130)
        self.Answer.configure(background="#26f7d4")
        self.Answer.configure(disabledforeground="#373737")
        self.Answer.configure(disabledbackground='#56fee2')
        # self.Answer.configure(font="TkFixedFont")
        self.Answer.configure(foreground="#000000")
        self.Answer.configure(highlightbackground="#26b467")
        self.Answer.configure(highlightcolor="#000000")
        self.Answer.configure(insertbackground="#000000")
        self.Answer.configure(selectbackground="blue")
        self.Answer.configure(selectforeground="white")
        self.Answer.delete(0, END)
        self.Answer.bind('<Return>', self.answer_enter_callback)
        self.Answer.config(state= "disabled")

        self.report = tk.Button(self.top,font = self.font_s)
        self.report.place(relx=0.04, rely=0.04, height=80, width=200)
        self.report.configure(activebackground="#ececec")
        self.report.configure(activeforeground="#000000")
        self.report.configure(background="#26f7d4")
        self.report.configure(disabledforeground="#373737")
        self.report.configure(foreground="#000000")
        self.report.configure(highlightbackground="#26b467")
        self.report.configure(highlightcolor="#26f7d4")
        self.report.configure(pady="0")
        self.report.configure(text='''Report''')
        self.report.configure(command=self.Report_callback)
        self.report.config(state= "disabled")

        self.Timer = tk.Label(self.top,font = self.font_s)
        self.Timer.place(relx=0.463, rely=0.04, height=80, width=300)
        self.Timer.configure(activebackground="#f9f9f9")
        self.Timer.configure(activeforeground="#26f7d4")
        self.Timer.configure(background="#26f7d4")
        self.Timer.configure(disabledforeground="#26f7d4")
        self.Timer.configure(foreground="#000000")
        self.Timer.configure(highlightbackground="#26b467")
        self.Timer.configure(highlightcolor="#26f7d4")
        #self.Timer.configure(insertbackground="#000000")
        self.Timer.configure(text='''Time:''')

        self.Start = tk.Button(self.top,font = self.font_s)
        self.Start.place(relx=0.05, rely=0.70, height=80, width=200)
        self.Start.configure(activebackground="#ececec")
        self.Start.configure(activeforeground="#000000")
        self.Start.configure(background="#26f7d4")
        self.Start.configure(disabledforeground="#373737")
        self.Start.configure(foreground="#000000")
        self.Start.configure(highlightbackground="#26b467")
        self.Start.configure(highlightcolor="#26f7d4")
        self.Start.configure(pady="0")
        self.Start.configure(text='''Start''')
        self.Start.configure(command=self.Start_callback)

        self.Pause = tk.Button(self.top,font = self.font_s)
        self.Pause.place(relx=0.323, rely=0.70, height=80, width=300)
        self.Pause.configure(activebackground="#ececec")
        self.Pause.configure(activeforeground="#000000")
        self.Pause.configure(background="#26f7d4")
        self.Pause.configure(disabledforeground="#373737")
        # self.Pause.configure(disabledbackground="#a3a3a3")
        self.Pause.configure(foreground="#000000")
        self.Pause.configure(highlightbackground="#26b467")
        self.Pause.configure(highlightcolor="#26f7d4")
        self.Pause.configure(pady="0")
        self.Pause.configure(text='''Pause''')
        self.Pause.configure(command=self.Pause_callback)
        self.Pause.config(state= "disabled")

        self.Stop = tk.Button(self.top,font = self.font_s)
        self.Stop.place(relx=0.73, rely=0.70, height=80, width=200)
        self.Stop.configure(activebackground="#ececec")
        self.Stop.configure(activeforeground="#000000")
        self.Stop.configure(background="#26f7d4")
        self.Stop.configure(disabledforeground="#373737")
        self.Stop.configure(foreground="#000000")
        self.Stop.configure(highlightbackground="#26b467")
        self.Stop.configure(highlightcolor="#26f7d4")
        self.Stop.configure(pady="0")
        self.Stop.configure(text='''Stop''')
        self.Stop.configure(command=self.Stop_callback)

        self.time_val = tk.IntVar()
        self.time_val.set(20)
        self.time = tk.Entry(self.top,font = self.font_s)
        self.time.place(relx=0.863, rely=0.04,height=80, width=100)
        self.time.configure(textvariable = self.time_val)
        self.time.configure(background="#26f7d4")
        self.time.configure(disabledforeground="#373737")
        self.time.configure(disabledbackground='#56fee2')
        # text.delete(0, END)
        # self.time.configure(font="TkFixedFont")
        self.time.configure(foreground="#000000")
        self.time.configure(insertbackground="#000000")


        self.rounds = tk.Entry(self.top,font = self.font_s)
        self.rounds_val = tk.IntVar()
        self.rounds_val.set(0)
        self.rounds.place(relx=0.293, rely=0.04,height=80, width=100)
        self.rounds.configure(background="#26f7d4")
        self.rounds.configure(disabledbackground='#56fee2')
        self.rounds.configure(disabledforeground="#373737")

        # self.time.configure(font="TkFixedFont")
        self.rounds_val = tk.IntVar()
        self.rounds_val.set(30)
        self.rounds.configure(textvariable = self.rounds_val)
        self.rounds.configure(foreground="#000000")
        self.rounds.configure(insertbackground="#000000")
        self.time_count = 20

    def generate_problem_list(self):
        if self.use_database:
            self.generate_problem_list_from_database()
        else:
            self.generate_problem_list_from_autoprogram()

    def generate_problem_list_from_autoprogram(self):
        self.Problem_list = []
        self.problem_index_list = []
        txt_list,answer_list,real_answer_list,correct_list,in_time_list = [],[],[],[],[]
        for i in range(get_val(self.rounds_val,10)):
            sign = self.signs[random.randint(0,len(self.signs)-1)]
            first_item = random.randint(self.first_num_range_down_boundary,
            self.first_num_range_up_boundary)
            second_item = random.randint(self.second_num_range_down_boundary,
            self.second_num_range_up_boundary)
            if sign=='-'and first_item<second_item:
                first_item,second_item = second_item,first_item
            txt = str(first_item) +sign +str(second_item) +'='
            answer = eval(txt[:-1])
            txt_list.append(txt)
            answer_list.append(answer)
            real_answer_list.append(-999)
            correct_list.append(0)
            in_time_list.append(1)
            self.problem_index_list.append('N')

        self.Problem_list.append(txt+str(answer))
        self.report_dict['problem'] = txt_list
        self.report_dict['correct_answer'] = answer_list
        self.report_dict['real_answer'] = real_answer_list
        self.report_dict['correct'] = correct_list
        self.report_dict['time'] = in_time_list
        self.report_dict['index_list'] = self.problem_index_list
    def generate_problem_list_from_database(self):
        self.Problem_list = []
        self.problem_index_list = []
        txt_list,answer_list,real_answer_list,correct_list,in_time_list = [],[],[],[],[]
        for i in range(get_val(self.rounds_val,10)):
            self.problem_index_list.append(random.randint(0,len(self.df)-1))
        for i in self.problem_index_list:
            txt = str(self.df['Num1'][i])+str(self.df['operator'][i])+str(self.df['Num2'][i])+'='
            answer = self.df['equal to'][i]
            txt_list.append(txt)
            answer_list.append(answer)
            real_answer_list.append(-999)
            correct_list.append(0)
            in_time_list.append(1)
            self.Problem_list.append(txt+str(answer))

        self.report_dict['problem'] = txt_list
        self.report_dict['correct_answer'] = answer_list
        self.report_dict['real_answer'] = real_answer_list
        self.report_dict['correct'] = correct_list
        self.report_dict['time'] = in_time_list
        self.report_dict['index_list'] = self.problem_index_list

    def Start_callback(self):
        print(self.problem_index)

        self.time_count = self.time_val.get()

        self.countdown()
        if self.problem_index ==0:
            self.report.config(state= "disabled")
            self.rounds_n = get_val(self.rounds_val,10)
            self.time.config(state= "disabled")
            self.generate_problem_list()
            self.Start.configure(text='''Next''')
            self.rounds.config(state= "disabled")
            txt_cur = self.report_dict['problem'][self.problem_index]
            self.Answer.config(state= "normal")
            self.Display_problem.configure(text=txt_cur)
        else:
            r = self.rounds_val.get()-1
            self.rounds_val.set(r)
            txt_pre = self.report_dict['problem'][self.problem_index-1]
            if self.problem_index<self.rounds_n:
                txt_cur = self.report_dict['problem'][self.problem_index]
                self.Display_problem.configure(text=txt_cur)

            elif self.problem_index==self.rounds_n:
                self.Start.configure(text='''Start''')
                self.Display_problem.configure(text='''a+b=''')
                try:
                    self.th.raise_exception()
                except:
                    print("no thread")
            answer_pre = self.report_dict['correct_answer'][self.problem_index-1]
            self.report_dict['real_answer'][self.problem_index-1] = get_val(self.Answer_val,-999)
            if get_val(self.Answer_val,-999)==answer_pre:
                self.report_dict['correct'][self.problem_index-1]=1
            else:
                self.report_dict['correct'][self.problem_index-1]=0

            self.report_dict['time'][self.problem_index-1]=int(self.time_count)-int(self.Timer.cget("text"))


        self.problem_index += 1
        self.Answer.delete(0, END)
 # set back status
        # print(get_val(self.rounds_val,10))
        if self.problem_index>self.rounds_n:
            self.Stop_callback()
            # self.problem_index =0
            # self.Answer.config(state= "disabled")
            # self.report_df = pd.DataFrame.from_dict(self.report_dict)
            # report_filename = self.generate_report_file_path()
            # self.report_df.to_csv(report_filename,index=False)

        # print(self.problem_index)
        # print(self.Problem_list)
        print('this is a test')
    def generate_report(self):
        pass

    def answer_enter_callback(self,event):
        self.Start_callback()


    def Report_callback(self):
        os.system('start excel '+'\"'+self.report_filename+'\"')
        path = self.generate_new_folder('M_report')
        plot_math_statistics(folder = path)


    def Pause_callback(self):
        if self.if_pause:
            self.Pause.configure(text='''Pause''')
        else:
            self.Pause.configure(text='''Continue''')
        self.if_pause = not self.if_pause


    # def Report_callback(self):




    def Stop_callback(self):
        self.problem_index =0
        self.Answer.config(state= "disabled")
        self.rounds.config(state= "normal")
        self.time.config(state= "normal")
        self.report_df = pd.DataFrame.from_dict(self.report_dict)
        self.report_filename = self.generate_report_file_path()
        self.report_df.to_csv(self.report_filename,index=False)
        self.report.config(state= "normal")
        self.Timer.configure(text='''Time''')
        self.Start.configure(text='''Start''')
        self.Display_problem.configure(text='''a+b=''')
        self.rounds_val.set(self.rounds_n)
        try:
            self.th.raise_exception()
        except:
            print("no thread")

    def countdown(self):
        try:
            self.th.raise_exception()
        except:
            print("no thread")
        self.th = thread_with_exception(self)
        self.th.start()

    def cd(self,ts):
        while ts > 0:
            self.Timer.config(text=ts)

            ts-=1
            # self.Timer.pack()
            time.sleep(1)
            if ts ==0:
                self.Timer.config(text='''Time out''')
                self.Timer.configure(foreground="red")

    def layout_widgets(self):
        self.math_problem_display.place(relx=0.26, rely=0.4, height=50, width=200)

    def main(self):
        self.top.mainloop()

    def generate_report_file_path(self):
        current_path = os.path.dirname(os.path.abspath(__file__))
        if not os.path.isdir(os.path.join(current_path, "M_report")):
            os.mkdir(os.path.join(current_path, "M_report"))
        save_path = os.path.join(current_path, "M_report")
        return os.path.join(save_path,datetime.datetime.now().strftime('%Y%m%d_%H%M%S')+'.csv')
def msg1(count):
    for i in range(count):
        index = random.randint(0,len(df))
        txt = str(df['Num1'][index])+str(df['operator'][index])+str(df['Num2'][index])+'='
        answer = simpledialog.askinteger("Input", txt,
                                        parent=ws)
        df['frequency'][index] += 1
        if df['equal to'][index]==answer:
            df['correct times'][index] += 1
        else:
            df['error times'][index] += 1
        df.to_csv('math_source.csv', index=False)
def go_back():
    df_backup.to_csv('math_source.csv', index=False)

def MathP():
    p = math_practice()
    p.main()

if __name__=='__main__':
    MathP()
