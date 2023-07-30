from flask import Flask
from flask import render_template
import pandas as pd
import folium
from flask import request

#インスタンス化
app = Flask(__name__,static_url_path='/static')

#ルーティング
#TOPページ
@app.route("/index",methods=['GET'])
def top():
    return render_template('index.html')

#検索結果ページ
#テキストの入力結果の反映＋CSV読み込み＆地図表示
@app.route("/search", methods=['POST'])
def station_name_and_map():
      text_station_name = request.form.get('station_name')
      text_minute = request.form.get('minute')
      df = pd.read_csv('data.csv')
      m = folium.Map(location=[df['緯度'].mean(), df['経度'].mean()], zoom_start=13)

      for index, row in df.iterrows():
         folium.Marker(
               location=[row['緯度'], row['経度']],
               popup=row['駅名'],
               tooltip=row['駅名']
         ).add_to(m)

        # 地図をHTML形式に変換してテンプレートに渡す
      map_html = m.get_root().render()
      return render_template('search.html', txt1=text_station_name, txt2=text_minute, map_html=map_html)

if __name__ == "__main__":
      app.run(debug=True, host="0.0.0.0", port=8000)