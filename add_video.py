#!/usr/bin/env python3
# ADD STUDIO VIDEO LAB PRO — ảnh + chữ + chuyển cảnh + nhạc nền, xuất MP4 dọc
import argparse, os, subprocess, tempfile, sys
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
import imageio_ffmpeg

W,H=540,960
PALETTES={
 "cyber":((67,246,232),(54,93,229),(7,22,45),(9,4,20)),
 "anime":((255,230,109),(255,61,134),(33,16,68),(7,11,29)),
 "matrix":((117,255,155),(0,180,123),(0,27,19),(2,8,7)),
 "pink":((255,103,200),(161,92,255),(38,11,42),(9,7,24)),
 "cinema":((157,201,255),(82,109,255),(11,25,50),(6,9,22))
}
def get_font(size,bold=False):
    paths=[r"C:\Windows\Fonts\arialbd.ttf" if bold else r"C:\Windows\Fonts\arial.ttf",
           "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]
    for p in paths:
        if os.path.exists(p):
            try:return ImageFont.truetype(p,size)
            except:pass
    return ImageFont.load_default()
def wrap(draw,text,font,maxw):
    out=[]; line=""
    for word in text.split():
        trial=(line+" "+word).strip()
        if draw.textbbox((0,0),trial,font=font)[2] <= maxw or not line:line=trial
        else:out.append(line);line=word
    if line:out.append(line)
    return out
def lerp(a,b,t):return tuple(int(a[i]*(1-t)+b[i]*t) for i in range(3))
def render_frame(images,title,subtitle,lines,t,duration,theme,transition,motion):
    accent,secondary,top,bottom=PALETTES[theme]
    # gradient base
    im=Image.new("RGB",(W,H));pix=im.load()
    for y in range(H):
        col=lerp(top,bottom,y/(H-1))
        for x in range(W):pix[x,y]=col
    n=max(1,len(lines));seg=duration/n;scene=min(n-1,int(t/seg));local=(t/seg)-scene
    if images:
        source=images[scene%len(images)]
        scale=max(W/source.width,H/source.height)*(1+.045*local)
        source=source.resize((int(source.width*scale),int(source.height*scale)),Image.Resampling.LANCZOS)
        x=(source.width-W)//2;y=(source.height-H)//2
        source=source.crop((x,y,x+W,y+H)).convert("RGB")
        source=ImageEnhance.Color(source).enhance(1.22)
        im=Image.blend(source,im,.50)
    # subtle grid and digital particles
    overlay=Image.new("RGBA",(W,H),(0,0,0,0));od=ImageDraw.Draw(overlay)
    for x in range(0,W,36):od.line((x,0,x,H),fill=(*accent,34),width=1)
    for y in range(0,H,36):od.line((0,y,W,y),fill=(*accent,28),width=1)
    for i in range(55):
        x=int((i*97+t*(70 if motion=="fast" else 18 if motion=="slow" else 38))%W)
        y=int((i*151+t*23)%H);od.rectangle((x,y,x+2,y+2),fill=(*accent,95))
    im=Image.alpha_composite(im.convert("RGBA"),overlay).convert("RGB")
    d=ImageDraw.Draw(im)
    d.rectangle((24,24,W-24,H-24),outline=accent,width=3)
    # glowing border by compositing a blurred outline
    glow=Image.new("RGBA",(W,H),(0,0,0,0));gd=ImageDraw.Draw(glow)
    gd.rectangle((24,24,W-24,H-24),outline=(*accent,170),width=5)
    im=Image.alpha_composite(im.convert("RGBA"),glow.filter(ImageFilter.GaussianBlur(9))).convert("RGB")
    d=ImageDraw.Draw(im)
    d.text((W//2,105),subtitle.upper(),font=get_font(20,True),fill=(238,246,255),anchor="mm")
    titlefont=get_font(42,True);title_lines=wrap(d,title.upper(),titlefont,W-70)
    y=int(H*.35)
    for text in title_lines[:3]:
        # layered glow text
        for dx,dy in [(-2,0),(2,0),(0,-2),(0,2)]:
            d.text((W//2+dx,y+dy),text,font=titlefont,fill=secondary,anchor="mm",stroke_width=1)
        d.text((W//2,y),text,font=titlefont,fill=accent,anchor="mm",stroke_width=1,stroke_fill=(4,8,20))
        y+=52
    content=lines[scene] if lines else "ADD STUDIO"
    f=get_font(27,True);yy=int(H*.64)
    alpha=1.0
    if transition=="fade":alpha=max(.15,min(1,local*5,(1-local)*5))
    if transition=="slide":yy+=int((1-local)*70)
    if transition=="zoom":
        # mild scale via font size
        f=get_font(max(18,int(27*(.82+.18*min(1,local*4)))),True)
    fill=tuple(int(v*alpha) for v in (245,249,255))
    for text in wrap(d,content,f,W-80)[:3]:
        d.text((W//2,yy),text,font=f,fill=fill,anchor="mm",stroke_width=1,stroke_fill=secondary);yy+=38
    if transition=="glitch" and local<.22:
        d.rectangle((40,yy-35,W-40,yy-31),fill=secondary)
        d.rectangle((65,yy+14,W-65,yy+17),fill=accent)
    d.text((W//2,H-65),"ADD STUDIO  //  VIDEO LAB PRO",font=get_font(17),fill=(190,208,232),anchor="mm")
    d.rectangle((45,H-45,W-45,H-41),fill=(65,75,95))
    d.rectangle((45,H-45,45+int((W-90)*min(1,t/duration)),H-41),fill=accent)
    return im
def main():
    p=argparse.ArgumentParser(description="ADD STUDIO Video Lab Pro")
    p.add_argument("--images",nargs="*",default=[],help="Đường dẫn ảnh JPG/PNG/WEBP")
    p.add_argument("--title",default="ADD STUDIO")
    p.add_argument("--subtitle",default="ENTER THE NEON WORLD")
    p.add_argument("--text",default="WELCOME TO ADD STUDIO|CREATE WITHOUT LIMITS|YOUR STORY STARTS HERE")
    p.add_argument("--duration",type=int,default=15)
    p.add_argument("--fps",type=int,default=24)
    p.add_argument("--theme",choices=PALETTES.keys(),default="cyber")
    p.add_argument("--transition",choices=["fade","slide","zoom","glitch"],default="fade")
    p.add_argument("--motion",choices=["slow","medium","fast"],default="medium")
    p.add_argument("--music",default=None,help="Đường dẫn nhạc nền MP3/WAV/M4A (tùy FFmpeg)")
    p.add_argument("--volume",type=float,default=.35,help="Âm lượng nhạc từ 0.0 đến 1.0")
    p.add_argument("--output",default="ADD_STUDIO_VIDEO_PRO.mp4")
    args=p.parse_args()
    if not 1<=args.duration<=180:p.error("--duration phải từ 1 đến 180")
    if not 10<=args.fps<=60:p.error("--fps phải từ 10 đến 60")
    if not 0<=args.volume<=1:p.error("--volume phải từ 0 đến 1")
    photos=[]
    for path in args.images:
        if os.path.isfile(path):
            try:photos.append(Image.open(path).convert("RGB"))
            except Exception as e:print(f"Bỏ qua ảnh {path}: {e}")
        else:print(f"Không tìm thấy ảnh: {path}")
    if args.music and not os.path.isfile(args.music):p.error(f"Không tìm thấy file nhạc: {args.music}")
    lines=[s.strip() for s in args.text.split("|") if s.strip()]
    ffmpeg=imageio_ffmpeg.get_ffmpeg_exe()
    output=os.path.abspath(args.output);os.makedirs(os.path.dirname(output),exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="add_studio_pro_") as tmp:
        raw=os.path.join(tmp,"frames.rgb")
        total=args.duration*args.fps
        print("\n=== ADD STUDIO VIDEO LAB PRO ===")
        print(f"Canvas {W}x{H} | {args.duration}s | {args.fps} FPS | theme={args.theme} | transition={args.transition}")
        with open(raw,"wb") as f:
            for i in range(total):
                frame=render_frame(photos,args.title,args.subtitle,lines,i/args.fps,args.duration,args.theme,args.transition,args.motion)
                f.write(frame.tobytes())
                if i%args.fps==0:print(f"\rĐang dựng hình: {i//args.fps}/{args.duration}s",end="",flush=True)
        print("\nĐang mã hóa MP4...")
        cmd=[ffmpeg,"-y","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(args.fps),"-i",raw]
        if args.music:
            cmd += ["-stream_loop","-1","-i",os.path.abspath(args.music)]
            cmd += ["-t",str(args.duration),"-map","0:v:0","-map","1:a:0","-c:a","aac","-b:a","160k","-af",f"volume={args.volume}"]
        else:cmd += ["-an"]
        cmd += ["-c:v","libx264","-preset","veryfast","-crf","20","-pix_fmt","yuv420p","-movflags","+faststart",output]
        try:subprocess.run(cmd,check=True)
        except subprocess.CalledProcessError:
            print("\nFFmpeg không thể xuất video. Hãy kiểm tra định dạng nhạc hoặc cài lại thư viện.")
            raise
    print(f"\nHoàn tất: {output}")
if __name__=="__main__":main()
