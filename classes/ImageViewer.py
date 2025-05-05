from classes.Utilities import *

class ImageViewer(TabFrame):
    _name = "Image Viewer"
    _description = "View images in .png and .gif formats."
    _icon = "image viewer icon.png"

    def init(self):
        self.tabname = "Image Viewer"
        self.images = [self.getPhotoimage("default-image.png")]
        self.imageIndex = 0
        self.imageLabel = ttk.Label(self)
        self.imageLabel.pack(expand=1, fill="both")
        self.currentImage = self.images[0]
        self.imageLabel.config(image=self.currentImage)
        self.buttonsFrame = ttk.Frame(self)
        self.buttonsFrame.pack()

        self.prevImageButton = ttk.Button(self, text="<<", command=self.prevImage)
        self.prevImageButton.pack(side="left", anchor="center")
        self.openImagesButton = ttk.Button(self, text="Open Image(s)", command=self.open)
        self.openImagesButton.pack(side="left", anchor="center")
        self.nextImageButton = ttk.Button(self, text=">>", command=self.nextImage)
        self.nextImageButton.pack(side="left", anchor="center")
        
        self.bind("<Left>", self.prevImage)
        self.bind("<Right>", self.nextImage)
    
    def open(self):
        paths = filedialog.askopenfilenames(
            title="Select PNG or GIF images",
            filetypes=[("Image Files", "*.png;*.gif")])
        if not paths:
            return
        self.imageIndex = 0
        self.images = []
        for imagepath in paths:
            self.images.append(tk.PhotoImage(file=imagepath))
        self.updateImage()
        CONFIGURATION.add_recent_file(paths[0])
    
    def updateImage(self):
        self.currentImage = self.images[self.imageIndex]
        self.imageLabel.config(image=self.currentImage)
    
    def nextImage(self) -> None:
        self.imageIndex += 1
        self.imageIndex %= len(self.images)
        self.updateImage()

    def prevImage(self) -> None:
        self.imageIndex -= 1
        self.imageIndex %= len(self.images)
        self.updateImage()
    
    def autoload(self, filepath):
        if not filepath or not os.path.isfile(filepath): return
        self.images = []
        self.images.append(tk.PhotoImage(file=filepath))
        self.imageIndex = 0
        self.updateImage()
        self.tabname = PFileHandler.get_filename_without_extension(filepath)
        CONFIGURATION.add_recent_file(filepath)