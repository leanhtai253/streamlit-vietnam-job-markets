import plotly.express as px
import streamlit.components.v1 as components
import plotly.graph_objects as go

class plot_functions:
    def bar_plot(self, df, x, y, title=None, orientation=None, color=None, color_continuous_scale=None, coloraxis=False,
          plot_bgcolor='white', height=1000, width=1000, xtitle=None, ytitle=None, barmode=None):
        mybar = px.bar(data_frame=df, x=x, y=y, orientation=orientation, color=color,
                  color_continuous_scale=color_continuous_scale, title=title,
                  height=height, barmode=barmode, width=width, text_auto=True)
        mybar.update_layout(yaxis={'categoryorder':'total ascending'}, coloraxis={'showscale':coloraxis},
                        plot_bgcolor=plot_bgcolor)
        
        if len(df[x]) <= 1:
            mybar.update_traces(width=0.2)
            mybar.update_layout(font=dict(size=20))
        mybar.update_traces(textposition='outside')
        mybar.update_xaxes(title=dict(text=xtitle, font=dict(size=20)), tickfont=dict(size=15))
        mybar.update_yaxes(title=dict(text=ytitle, font=dict(size=20)), tickfont=dict(size=15))
        mybar.update_layout(title=dict(font=dict(size=25)))
        return mybar
    
    def map_plot(self, geojson, locations, z, hover_provinces, title=None, colorscale=None):
        trace = go.Choroplethmapbox(
            geojson = geojson,
            featureidkey= 'properties.Code',
            locations = locations,
            z = z,
            hovertext = hover_provinces,
            colorscale = colorscale,
            marker_opacity=0.9,
            marker_line_width=0.9,
            showscale=True
        )
        layout = go.Layout(
            title=title,
            height=900,
            width=900,  
            mapbox=dict(
            style='white-bg',
            center=dict(
                lat=17,  
                lon=106 
            ),
            zoom=4.5
            ),
        )
        return ({
            'data': [trace],
            'layout': layout
        })