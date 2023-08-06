class caption():
    def load_demo_image(image_size,device,image_path):
        from torchvision import transforms
        from torchvision.transforms.functional import InterpolationMode
        from PIL import Image
        #image_path = '2.png' 
        #raw_image = Image.open(requests.get(img_url, stream=True).raw).convert('RGB') 
        raw_image = Image.open(image_path).convert('RGB')
        w,h = raw_image.size
        #display(raw_image.resize((w//5,h//5)))        
        transform = transforms.Compose([
            transforms.Resize((image_size,image_size),interpolation=InterpolationMode.BICUBIC),
            transforms.ToTensor(),
            transforms.Normalize((0.48145466, 0.4578275, 0.40821073), (0.26862954, 0.26130258, 0.27577711))
            ]) 
        image = transform(raw_image).unsqueeze(0).to(device)   
        return image
    def read_image():
        image_size = 384
        #filename='2.jpg'
        from models.blip import blip_decoder
        image = load_demo_image(image_size=image_size, device=device,image_path=image_path)
        model_url = 'https://storage.googleapis.com/sfr-vision-language-research/BLIP/models/model_large_caption.pth'    
        model = blip_decoder(pretrained=model_url, image_size=384, vit='large')
        model.eval()
        model = model.to(device)
        with torch.no_grad():
            # beam search
            caption = model.generate(image, sample=False, num_beams=3, max_length=20, min_length=5) 
            # nucleus sampling
            # caption = model.generate(image, sample=True, top_p=0.9, max_length=20, min_length=5) 
            return caption[0]