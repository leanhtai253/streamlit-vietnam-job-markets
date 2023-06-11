import plotly.express as px
import streamlit.components.v1 as components

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
    
    def mermaid(self, code: str) -> None:
        return f"""
            <div class="mermaid">
                {code}
            </div>

            <script type="module">
                import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
                mermaid.initialize({{ startOnLoad: true }});
            </script>
            """