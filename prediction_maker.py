import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from PIL import ImageTk, Image

from statsmodels.tsa.holtwinters import ExponentialSmoothing
import statsmodels.api as sm

from tkinter import *
from tkinter import ttk
import webbrowser


argument_01 = ""
argument_02 = ""
argument_03 = ""
argument_04 = 0
argument_05 = ""

argument_07 = 0
argument_08 = 0
argument_09 = 0
argument_10 = 0
argument_11 = ""

root = Tk()
root.title("Forecast Oracle")
root.geometry("1150x470")
root.iconbitmap('release_introduction_debut_product_launch_icon_263002.ico')

def load_dataset():
    df = sns.load_dataset("flights")
    Label(root, text="Fájl vizsgálatra előkészítve ✅").grid(row=15, column=0, sticky="w")
    return df

df = load_dataset()

def callback(url):
    webbrowser.open_new(url)

def save_variables():
    global argument_01, argument_02, argument_03, argument_04, argument_05, argument_07, argument_08, argument_09, argument_10, argument_11
    argument_01 = e_1.get()
    argument_02 = combo_trend.get()
    argument_03 = combo_seasonal.get()
    argument_04 = int(e_4.get())
    argument_05 = combo_damped_trend.get() == "True"

    argument_07 = float(e_7.get())
    argument_08 = float(e_8.get())
    argument_09 = float(e_9.get())
    argument_10 = float(e_10.get())
    argument_11 = combo_remove_bias.get() == "True"

    Label(root, text="Beállított értékek elmentve").grid(row=17, column=0, columnspan=2, sticky="w")

def calculation():
    """Exponentival smoothing: build the model, fit the model, print the result"""
    model = ExponentialSmoothing(
        endog=df[argument_01],
        trend=argument_02,
        damped_trend=argument_05,
        seasonal=argument_03,
        seasonal_periods=argument_04
    )

    fitted_model = model.fit(
        smoothing_level=argument_07,
        smoothing_trend=argument_08,
        smoothing_seasonal=argument_09,
        damping_slope=argument_10,
        remove_bias=argument_11
    )

    predict_length = len(df['passengers']) + 12
    predictions = fitted_model.predict(start=0, end=predict_length - 1)

    new_index = pd.RangeIndex(start=0, stop=predict_length)
    df_extended = pd.DataFrame(index=new_index)
    df_extended['predict'] = predictions
    df_extended.loc[:len(df) - 1, 'passengers'] = df['passengers']

    display_results(df_extended[::-1])  # reverse the dataframe
    show_result(df_extended)  # plot the result

def show_result(df_extended):
    plt.figure(figsize=(14, 7))
    plt.plot(df_extended['passengers'], label='Actual Data')
    plt.plot(df_extended['predict'], label='Predicted Data', color='grey', linestyle='--')
    plt.legend()
    plt.title('Tény és Előrejelzés')
    plt.xlabel('Index')
    plt.ylabel('Passengers')
    plt.grid(True)
    plt.show()

def display_results(df_extended):
    new_window = Toplevel(root)
    new_window.title("Előrejelzés Eredmények")
    new_window.geometry("600x350")

    frame = Frame(new_window)
    frame.pack(fill=BOTH, expand=True)

    tree = ttk.Treeview(frame, columns=list(df_extended.columns), show='headings')
    vsb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=vsb.set)
    vsb.pack(side=RIGHT, fill=Y)

    for col in df_extended.columns:
        tree.heading(col, text=col)
        tree.column(col, width=100)
    for row in df_extended.itertuples(index=False):
        tree.insert("", "end", values=row)

    tree.pack(fill=BOTH, expand=True)

# Widgetek létrehozása
myLabel_title = Label(root, text="Az argumentumok változtatásával az exponenciális simítási modell különböző aspektusait,\nmint a trend, szezonális hatások és csillapítás mértéke, lehet finomhangolni,\namely lehetővé teszi a modell pontosságának és adaptációs képességének optimalizálását\naz időbeli előrejelzésekhez.", justify="left")
myLabel_title.grid(row=0, column=0, columnspan=2, sticky="w")

myLabel_1 = Label(root, text='column_name:')
myLabel_1.grid(row=1, column=0, sticky='w')
e_1 = Entry(root, width=10, borderwidth=3)
e_1.insert(0, "passengers")  # Helyes érték beállítása
e_1.grid(row=1, column=1, sticky="w")
myLabel_1_explanation = Label(root, text = "Az idősor adatok, amelyeket a modellhez használunk. Ez az adatforrás, amely alapján a modell előrejelzéseket készít.")
myLabel_1_explanation.grid(row=1, column=3, sticky="w")

myLabel_2 = Label(root, text='trend:')
myLabel_2.grid(row=2, column=0, sticky='w')
combo_trend = ttk.Combobox(root, values=["add", "mul"], width=7)
combo_trend.set("add")
combo_trend.grid(row=2, column=1, sticky="w")
myLabel_2_explanation = Label(root, text = "Meghatározza, hogy a modell tartalmazzon-e trendkomponenst, hosszútávó növekedés vagy csökkenés.")
myLabel_2_explanation.grid(row=2, column=3, sticky="w")

myLabel_3 = Label(root, text='seasonal:')
myLabel_3.grid(row=3, column=0, sticky='w')
combo_seasonal = ttk.Combobox(root, values=["add", "mul"], width=7)
combo_seasonal.set("mul")
combo_seasonal.grid(row=3, column=1, sticky="w")
myLabel_3_explanation = Label(root, text = "Meghatározza a szezonális komponens típusát, amely leírja az adatok periodikus változásait.")
myLabel_3_explanation.grid(row=3, column=3, sticky="w")

myLabel_4 = Label(root, text='seasonal_periods:')
myLabel_4.grid(row=4, column=0, sticky='w')
e_4 = Entry(root, width=10, borderwidth=3)
e_4.insert(0, 12)
e_4.grid(row=4, column=1, sticky="w")
myLabel_4_explanation = Label(root, text = "A szezonális időszakok száma. Ez határozza meg, hogy hány megfigyelés alkot egy teljes szezonális ciklust.")
myLabel_4_explanation.grid(row=4, column=3, sticky="w")

myLabel_5 = Label(root, text='damped_trend:')
myLabel_5.grid(row=5, column=0, sticky='w')
combo_damped_trend = ttk.Combobox(root, values=["True", "False"], width=7)
combo_damped_trend.set("False")
combo_damped_trend.grid(row=5, column=1, sticky="w")
myLabel_5_explanation = Label(root, text = " Ha igaz, akkor a trendkomponens csillapított lesz, azaz a trend idővel fokozatosan kisimul.")
myLabel_5_explanation.grid(row=5, column=3, sticky="w")

myLabel_6 = Label(root, text=10*'--')
myLabel_6.grid(row=6, column=0, sticky='w')

myLabel_7 = Label(root, text='smoothing level:')
myLabel_7.grid(row=8, column=0, sticky='w')
e_7 = Entry(root, width=10, borderwidth=3)
e_7.grid(row=8, column=1, sticky="w")
e_7.insert(0, 0.2)
myLabel_7_explanation = Label(root, text = "[0,1] Alfa paraméter, mely megadja a régebbi és újabb adatok milyen egyensúlyban hassanak az előrejelzésre.")
myLabel_7_explanation.grid(row=8, column=3, sticky="w")

myLabel_8 = Label(root, text='smoothing trend:')
myLabel_8.grid(row=9, column=0, sticky='w')
e_8 = Entry(root, width=10, borderwidth=3)
e_8.grid(row=9, column=1, sticky="w")
e_8.insert(0, 0.2)
myLabel_8_explanation = Label(root, text = "[0,1] Béta paraméter mely az időben átfogóbb illetve újabb trendszerű mozgások reaktivitását szabályozza.")
myLabel_8_explanation.grid(row=9, column=3, sticky="w")

myLabel_9 = Label(root, text='smoothing seasonal:')
myLabel_9.grid(row=10, column=0, sticky='w')
e_9 = Entry(root, width=10, borderwidth=3)
e_9.grid(row=10, column=1, sticky="w")
e_9.insert(0, 0.2)
myLabel_9_explanation = Label(root, text = "[0,1] Gammar érték: Szeoznális hatások exponenciális simításának szintje.")
myLabel_9_explanation.grid(row=10, column=3, sticky="w")

myLabel_10 = Label(root, text='damping slope:')
myLabel_10.grid(row=11, column=0, sticky='w')
e_10 = Entry(root, width=10, borderwidth=3)
e_10.grid(row=11, column=1, sticky="w")
e_10.insert(0, 0.99)
myLabel_11_explanation = Label(root, text = "[0,1] Simítási együttható, mely meghatározza a trend simításának mértékét.")
myLabel_11_explanation.grid(row=11, column=3, sticky="w")

myLabel_11 = Label(root, text='remove bias:')
myLabel_11.grid(row=12, column=0, sticky='w')
combo_remove_bias = ttk.Combobox(root, values=["True", "False"], width=7)
combo_remove_bias.set("False")
combo_remove_bias.grid(row=12, column=1, sticky="w")
myLabel_line = Label(root, text=10*'--')
myLabel_line.grid(row=13, column=0, sticky='w')
myLabel_2_explanation = Label(root, text = "Ha igaz, eltávolítja az esetleges előrejelzési torzítást a becslésekből.")
myLabel_2_explanation.grid(row=12, column=3, sticky="w")

# Gombok létrehozása és elhelyezése
button_width = 30
Button(root, text="Értékek mentése", width=button_width, pady=8, fg="blue", command=save_variables).grid(row=16, column=0, columnspan=2)
Button(root, text="Forecast", width=button_width, pady=8, fg="blue", command=calculation).grid(row=18, column=0, columnspan=2)

# help link
link1 = Label(root, text="Help", fg="blue", cursor="hand2")
link1.grid(row=19, column=0, sticky="w")
link1.bind("<Button-1>", lambda e: callback("https://www.linkedin.com/in/mezoltan/"))

# start
root.mainloop() 