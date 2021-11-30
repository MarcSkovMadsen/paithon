import gradio as gr

def video_flip(video):
    return video

iface = gr.Interface(
    video_flip,
    "video",
    "playable_video"
)

iface.launch()