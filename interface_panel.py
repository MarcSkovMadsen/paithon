import param
import panel as pn

def video_flip(video):
    return video

class VideoModel(Model):
    video = param.Video()

    def predict(self):
        return video_flip(self.video)

Interface(
    model=Model,
    inputs={"video": pn.widgets.VideoInput()} # Optional
    outputs = [pn.pane.Video()]
).servable()