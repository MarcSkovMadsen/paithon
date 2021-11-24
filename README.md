![Paithon Logo](https://raw.githubusercontent.com/MarcSkovMadsen/paithon/master/assets/images/paithon-logo.png)

[![PyPI version](https://badge.fury.io/py/paithon.svg)](https://pypi.org/project/paithon/) [![Downloads](https://pepy.tech/badge/paithon/month)](https://pepy.tech/project/paithon) ![Python Versions](https://img.shields.io/badge/python-3.6%20%7C%203.7%20%7C%203.8%20%7C%203.9-blue) ![PyPI - License](https://img.shields.io/pypi/l/paithon) ![Style Black](https://warehouse-camo.ingress.cmh1.psfhosted.org/fbfdc7754183ecf079bc71ddeabaf88f6cbc5c00/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f636f64652532307374796c652d626c61636b2d3030303030302e737667)

[![Follow on Twitter](https://img.shields.io/twitter/follow/MarcSkovMadsen.svg?style=social)](https://twitter.com/MarcSkovMadsen)

# &#129504; Paithon

PRE-ALPHA STATE

**Make your AI models interactive in no time**. Easy to use examples and components for the Jupyter Notebook, your favorite Editor/ IDE and your next AI App.

*Paithon* is **Panel AI Tools with Humor ON**. Get started now!

| Jupyter Labs | Apps |
| - | - |
| [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/marcskovmadsen/paithon/HEAD?urlpath=lab/tree/examples) | [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/marcskovmadsen/paithon/HEAD?urlpath=panel) |

![Paithon Tour](assets/videos/paithon-tour.gif)

## 🏃 Getting Started

With `pip`

```bash
pip install paithon
```

From within a Jupyter Notebook

```python
import paithon as pa
import panel as pn

pn.extension()
```

### 👩‍🏫 Reference Guides

| Guide | Notebook | Jupyter Labs | Apps |
| - | - | - | - |
| DocStringViewer | [View](https://github.com/MarcSkovMadsen/paithon/blob/master/examples/reference/shared/pane/DocStringViewer.ipynb) | [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/marcskovmadsen/paithon/HEAD?urlpath=lab/tree/examples/reference/shared/pane/DocStringViewer.ipynb) | [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/marcskovmadsen/paithon/HEAD?urlpath=panel/DocStringViewer) |
| ImageInput | [View](https://github.com/MarcSkovMadsen/paithon/blob/master/examples/reference/image/widgets/ImageInput.ipynb) | [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/marcskovmadsen/paithon/HEAD?urlpath=lab/tree/examples/reference/image/widgets/ImageInput.ipynb) | [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/marcskovmadsen/paithon/HEAD?urlpath=panel/ImageInput) |

## 🏁 Background

I believe that Panel is a very flexible and powerful tool compared to the other python ML app frameworks out there. I believe it can give you and your AI team super powers.

So I started this project to help you and the Panel framework. As a bonus I will learn more about AI.

## ⚖️ License

The `paithon` package and repository is open source and free to use (MIT License).

## 💡 Inspiration

I find inspiration at

- [Hugging Face Widgets](https://github.com/huggingface/huggingface_hub/tree/main/widgets)
- [Gradio](https://gradio.app/)
- [Panel](https://panel.holoviz.org)

## 🛣️ Roadmap

When I get the time I would like to

- Support common workflows in ML and DL.
- Implement Panel versions of the Hugging Face widgets
- Show that Panel can easily do what Gradio can and so much more.
- Add badges for 100% test coverage etc.
- Distribute as conda package

## 📰 Change Log

- 0.0.3: Fix some broken links
- 0.0.2: Add ImageInput and DocStringViewer
- 0.0.1: First Version
