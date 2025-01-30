from PIL import ImageTk, ImageEnhance


def highlight(image, button, factor=1.15):
    def animate(widget, hover=True):
        if hover:
            # brightens the image by 1.1x, then converts to tk image
            new_image = ImageTk.PhotoImage(ImageEnhance.Brightness(image).enhance(factor))
            widget.config(image=new_image)
            widget.image = new_image  # makes the image load for some reason
        else:
            new_image = ImageTk.PhotoImage(image)
            widget.config(image=new_image)
            widget.image = new_image

    def on_hover(event):
        animate(event.widget)

    def on_leave(event):
        animate(event.widget, False)

    button.bind("<Enter>", on_hover)
    button.bind("<Leave>", on_leave)
