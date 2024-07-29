from flask import Flask, render_template, request
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objs as go

app = Flask(__name__)

# Configurar el entorno Jinja2 para incluir zip
app.jinja_env.globals.update(zip=zip)

# Cargar datos
df = pd.read_csv('vgsales.csv')

# Obtener los géneros únicos y sus imágenes correspondientes
genres = df['Genre'].unique()
genre_images = {
    'Action': 'img/action.jpg',
    'Sports': 'img/sports.jpg',
    'Shooter': 'img/shooter.jpg',
    'Role-Playing': 'img/role_playing.jpg',
    'Platform': 'img/platform.jpg',
    'Misc': 'img/misc.jpg',
    'Racing': 'img/racing.jpg',
    'Fighting': 'img/fighting.jpg',
    'Simulation': 'img/simulation.jpg',
    'Puzzle': 'img/puzzle.jpg',
    'Adventure': 'img/adventure.jpg',
    'Strategy': 'img/strategy.jpg'
}

# Generar gráficos y tablas
def generate_graphs():
    # Ventas por año
    yearly_sales = df.groupby('Year')['Global_Sales'].sum()
    yearly_sales_plotly = go.Figure(data=[
        go.Scatter(x=yearly_sales.index, y=yearly_sales.values, mode='lines+markers')
    ])
    yearly_sales_plotly.update_layout(title='Ventas Globales por Año', xaxis_title='Año', yaxis_title='Ventas Globales')
    yearly_sales_div = yearly_sales_plotly.to_html(full_html=False)

    # Ventas por plataforma
    platform_sales = df.groupby('Platform')['Global_Sales'].sum().sort_values(ascending=False)
    platform_sales_plotly = px.bar(platform_sales, x=platform_sales.index, y=platform_sales.values, labels={'x': 'Plataforma', 'y': 'Ventas Globales'})
    platform_sales_plotly.update_layout(title='Ventas Globales por Plataforma', xaxis_title='Plataforma', yaxis_title='Ventas Globales')
    platform_sales_div = platform_sales_plotly.to_html(full_html=False)

    return yearly_sales_div, platform_sales_div

# Top 5 juegos más jugados en cada año
top_games_by_year = df.groupby('Year').apply(
    lambda x: x.nlargest(5, 'Global_Sales', keep='all')).reset_index(drop=True)

# Convertir los datos en un diccionario para facilitar la renderización en HTML
top_games_dict = top_games_by_year.groupby('Year')[['Name', 'Global_Sales', 'Platform']].apply(lambda x: x.to_dict(orient='records')).to_dict()

# Juegos organizados por empresa
publisher_games = df.groupby('Publisher')['Name'].apply(list).to_dict()

# Juegos más vendidos
most_sold_games = df.nlargest(
    10, 'Global_Sales')[['Name', 'Global_Sales', 'Platform']]
most_sold_games_table = most_sold_games.to_html(classes='data', index=False)

# Añadir imágenes a los juegos más vendidos
most_sold_images = [f'img/mss/ms{i+1}.jpg' for i in range(10)]

# Juegos más jugados (por ventas globales)
most_played_games = df.nlargest(10, 'Global_Sales')[['Name', 'Global_Sales']]
most_played_games_table = most_played_games.to_html(classes='data',
                                                    index=False)

# Añadir imágenes a los juegos más jugados
most_played_images = [f'img/mp{i+1}.jpg' for i in range(10)]

# Juegos por género
games_by_genre = df.groupby('Genre', group_keys=False).apply(
    lambda x: x.nlargest(5, 'Global_Sales', keep='all')).reset_index(drop=True)

# Gráficos de ventas
fig, axes = plt.subplots(1, 3, figsize=(24, 8))

# Ventas por año
yearly_sales = df.groupby('Year')['Global_Sales'].sum()
axes[0].plot(yearly_sales.index, yearly_sales.values)
axes[0].set_title('Ventas globales por año')

# Ventas por plataforma
platform_sales = df.groupby('Platform')['Global_Sales'].sum().sort_values(
    ascending=False)
sns.barplot(x=platform_sales.index,
            y=platform_sales.values,
            ax=axes[1],
            palette='viridis')
axes[1].set_title('Ventas globales por plataforma')

# Ventas regionales
regions = ['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales', 'Global_Sales']
games_count = df[regions].apply(lambda x: (x > 0).sum()).sort_values(
    ascending=False)
sns.barplot(x=games_count.index,
            y=games_count.values,
            ax=axes[2],
            palette='viridis')
axes[2].set_title('Cantidad de juegos por región')

plt.tight_layout()
plt.savefig('static/plots/summary.png')

# Distribución de juegos por plataforma
plt.figure(figsize=(12, 8))
sns.countplot(data=df,
              x='Platform',
              order=df['Platform'].value_counts().index,
              palette='viridis')
plt.title('Distribución de juegos por plataforma')
plt.savefig('static/plots/platform_distribution.png')

# Gráfico interactivo de ventas globales por plataforma usando Plotly
platform_sales_plotly = px.bar(platform_sales,
                               x=platform_sales.index,
                               y=platform_sales.values,
                               labels={
                                   'x': 'Plataforma',
                                   'y': 'Ventas Globales'
                               })
platform_sales_plotly.update_layout(title='Ventas Globales por Plataforma',
                                    xaxis_title='Plataforma',
                                    yaxis_title='Ventas Globales')
platform_sales_div = platform_sales_plotly.to_html(full_html=False)

# Gráfico interactivo de ventas globales por año usando Plotly
yearly_sales_plotly = go.Figure(data=[
    go.Scatter(
        x=yearly_sales.index, y=yearly_sales.values, mode='lines+markers')
])
yearly_sales_plotly.update_layout(title='Ventas Globales por Año',
                                  xaxis_title='Año',
                                  yaxis_title='Ventas Globales')
yearly_sales_div = yearly_sales_plotly.to_html(full_html=False)

# Gráfico interactivo de ventas globales por género usando Plotly
genre_sales = df.groupby('Genre')['Global_Sales'].sum().sort_values(ascending=False)
genre_sales_plotly = px.bar(genre_sales, x=genre_sales.index, y=genre_sales.values, labels={'x': 'Género', 'y': 'Ventas Globales'})
genre_sales_plotly.update_layout(title='Ventas Globales por Género', xaxis_title='Género', yaxis_title='Ventas Globales')
genre_sales_div = genre_sales_plotly.to_html(full_html=False)


@app.route('/')
def index():
    return render_template('index.html',
                           genres=genres,
                           genre_images=genre_images,
                           current_page='/')


@app.route('/most_sold')
def most_sold():
    return render_template('most_sold.html',
                           games=most_sold_games.to_dict('records',),
                           images=most_sold_images,
                           current_page='/most_sold')


@app.route('/most_played')
def most_played():
    return render_template('most_played.html',
                           games=most_played_games.to_dict('records'),
                           images=most_played_images,
                           current_page='/most_played')


@app.route('/top_games')
def top_games():
    return render_template('top_games.html',
                           top_games_by_year=top_games_dict,
                           current_page='/top_games')


@app.route('/publishers')
def publishers():
    return render_template('publishers.html',
                           publisher_games=publisher_games,
                           current_page='/publishers')


@app.route('/statistics')
def statistics():
    return render_template('statistics.html',
                           plot_div1=yearly_sales_div,
                           plot_div2=platform_sales_div,
                           plot_div3=genre_sales_div,
                           current_page='/statistics')


@app.route('/genre/<genre_name>')
def genre(genre_name):
    genre_games = games_by_genre[games_by_genre['Genre'] == genre_name][[
        'Name', 'Global_Sales'
    ]]
    genre_games_table = genre_games.to_html(classes='data', index=False)
    return render_template('genre.html',
                           genre=genre_name,
                           table=genre_games_table,
                           current_page='/genre/{}'.format(genre_name))


@app.route('/data')
def data():
    # Datos de juegos más vendidos
    most_sold_games = df.nlargest(10, 'Global_Sales')[['Name', 'Global_Sales', 'Platform']]
    most_sold_games_table = most_sold_games.to_html(classes='data', index=False)

    # Datos de juegos más jugados (por ventas globales)
    most_played_games = df.nlargest(10, 'Global_Sales')[['Name', 'Global_Sales', 'Platform']]
    most_played_games_table = most_played_games.to_html(classes='data', index=False)

    # Datos de empresas con más ventas
    top_publishers = df.groupby('Publisher')['Global_Sales'].sum().sort_values(ascending=False).head(10).reset_index()
    top_publishers_table = top_publishers.to_html(classes='data', index=False)
    # Juego más sobresaliente
    top_game = df.nlargest(1, 'Global_Sales')[['Name', 'Global_Sales', 'Platform']]
    top_game_image = 'top_game.jpg'
    top_game_name = top_game.iloc[0]['Name']

    # Región con mayor número de jugadores
    region_sales = df[['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales']].sum()
    top_region = region_sales.idxmax()
    top_region_sales = region_sales.max()

    # Plataforma con más juegos
    platform_games = df['Platform'].value_counts().idxmax()
    platform_games_count = df['Platform'].value_counts().max()

    # Plataforma con más ventas
    platform_sales = df.groupby('Platform')['Global_Sales'].sum().idxmax()
    platform_sales_amount = df.groupby('Platform')['Global_Sales'].sum().max()

    # Gráficos interactivos
    yearly_sales_div, platform_sales_div = generate_graphs()

    return render_template('data.html',  most_sold_table=most_sold_games_table, 
       most_played_table=most_played_games_table, 
       top_publishers_table=top_publishers_table,
       top_game_name=top_game_name,
       top_game_image=top_game_image,
       top_region=top_region,
       top_region_sales=top_region_sales,
       platform_games=platform_games,
       platform_games_count=platform_games_count,
       platform_sales=platform_sales,
       platform_sales_amount=platform_sales_amount,
       plot_div1=yearly_sales_div,
       plot_div2=platform_sales_div,
       current_page='/data')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
