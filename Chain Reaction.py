# Play Screen

import pygame
import numpy as np
import random
from pygame.locals import *

pygame.init()

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

disInfo = pygame.display.Info()
monw=disInfo.current_w
monh=disInfo.current_h
aspr=monw/monh
dw = 800
dh = int(dw/aspr)

disWin = pygame.display.set_mode((dw, dh), pygame.RESIZABLE)
pygame.display.set_caption("Chain Reaction")

state = 0
phase = 0
clock = pygame.time.Clock()
viba=0
vib=[-1, 0, 1, 2, 1, 0]
rot2x1=[-13, -17, -18, -17, -13, -7, 0, 7, 13, 17, 18, 17, 13, 7, 0, -7]
rot2y1=[-13, -7, 0, 7, 13, 17, 18, 17, 13, 7, 0, -7, -13, -17, -18, -17]
rot2x2=[13, 17, 18, 17, 13, 7, 0, -7, -13, -17, -18, -17, -13, -7, 0, 7]
rot2y2=[13, 7, 0, -7, -13, -17, -18, -17, -13, -7, 0, 7, 13, 17, 18, 17]
rot3x1=[0, -6, -12, -17, -21, -23, -24, -23, -21, -17, -12, -6, 0, 6, 12, 17, 21, 23, 24, 23, 21, 17, 12, 6]
rot3y1=[-24, -23, -21, -17, -12, -6, 0, 6, 12, 17, 21, 23, 24, 23, 21, 17, 12, 6, 0, -6, -12, -17, -21, -23]
rot3x2=[-21, -17, -12, -6, 0, 6, 12, 17, 21, 23, 24, 23, 21, 17, 12, 6, 0, -6, -12, -17, -21, -23, -24, -23]
rot3y2=[12, 17, 21, 23, 24, 23, 21, 17, 12, 6, 0, -6, -12, -17, -21, -23, -24, -23, -21, -17, -12, -6, 0, 6]
rot3x3=[21, 23, 24, 23, 21, 17, 12, 6, 0, -6, -12, -17, -21, -23, -24, -23, -21, -17, -12, -6, 0, 6, 12, 17]
rot3y3=[12, 6, 0, -6, -12, -17, -21, -23, -24, -23, -21, -17, -12, -6, 0, 6, 12, 17, 21, 23, 24, 23, 21, 17]
gameExit = False
fullscreen = False
r=9
c=16
abx=[-1, 1]
cnt=0
player=[red, green]

def dis(a, b, mode):
    disWin = pygame.display.set_mode((a, b), mode)

def grid(a, b, c, d, col, mode):
    for x in range(1, a):
        if mode:
            pygame.draw.line(disWin, col, (0, 108+int((864*x)/a)), (c, 108+int((864*x)/a)))
        else:
            pygame.draw.line(disWin, col, (0, int(d*x)/a), (c, int(d*x)/a))
    for x in range(1, b):
        if mode:
            pygame.draw.line(disWin, col, (192+int((1536*x)/b), 0), (192+int((1536*x)/b), d))
        else:
            pygame.draw.line(disWin, col, (int((c*x)/b), 0), (int((c*x)/b), d))

def move(x, y, a, b, cnt,  mode):
    if mode:
        if cnt==0 and arr[int((y-108)/int(864/r))][int((x-192)/int(1536/c))]>=0:
            arr[int((y-108)/int(864/r))][int((x-192)/int(1536/c))]+=1
            rxn(int((y-108)/int(864/r)), int((x-192)/int(1536/c)))
            cnt=(cnt+1)%2
        elif cnt==1 and arr[int((y-108)/int(864/r))][int((x-192)/int(1536/c))]<=0:
            arr[int((y-108)/int(864/r))][int((x-192)/int(1536/c))]-=1
            rxn(int((y-108)/int(864/r)), int((x-192)/int(1536/c)))
            cnt=(cnt+1)%2
    else:
        if cnt==0 and arr[int(y/int(b/r))][int(x/int(a/c))]>=0:
            arr[int(y/int(b/r))][int(x/int(a/c))]+=1
            rxn(int(y/int(b/r)), int(x/int(a/c)))
            cnt=(cnt+1)%2
        elif cnt==1 and arr[int(y/int(b/r))][int(x/int(a/c))]<=0:
            arr[int(y/int(b/r))][int(x/int(a/c))]-=1
            rxn(int(y/int(b/r)), int(x/int(a/c)))
            cnt=(cnt+1)%2
    return cnt

def shmv(a, b, v, mode):
    if mode:
        for i in range(0, r):
            for j in range(0, c):
                if(arr[i][j]==1):
                    pygame.draw.circle(disWin, red, (192+int((1536*j)/c)+int(int(1536/c)/2)+v*ran[i][j], 108+int((864*i)/r)+int(int(864/r)/2)), int(min(int(864/r), int(1536/c))/4))
                elif(arr[i][j]==-1):
                    pygame.draw.circle(disWin, green, (192+int((1536*j)/c)+int(int(1536/c)/2)+v*ran[i][j], 108+int((864*i)/r)+int(int(864/r)/2)), int(min(int(864/r), int(1536/c))/4))
                elif(arr[i][j]==2):
                    pygame.draw.circle(disWin, red, (192+int((1536*j)/c)+int(int(1536/c)/2)+int((int(min(int(864/r), int(1536/c))/4)*rot2x1[(rota[i][j]*rot2[i][j])%16])/25)+v*ran[i][j], 108+int((864*i)/r)+int(int(864/r)/2)+int((int(min(int(864/r), int(1536/c))/4)*rot2y1[(rota[i][j]*rot2[i][j])%16])/25)), int(min(int(864/r), int(1536/c))/4))
                    pygame.draw.circle(disWin, red, (192+int((1536*j)/c)+int(int(1536/c)/2)+int((int(min(int(864/r), int(1536/c))/4)*rot2x2[(rota[i][j]*rot2[i][j])%16])/25)+v*ran[i][j], 108+int((864*i)/r)+int(int(864/r)/2)+int((int(min(int(864/r), int(1536/c))/4)*rot2y2[(rota[i][j]*rot2[i][j])%16])/25)), int(min(int(864/r), int(1536/c))/4))
                elif(arr[i][j]==-2):
                    pygame.draw.circle(disWin, green, (192+int((1536*j)/c)+int(int(1536/c)/2)+int((int(min(int(864/r), int(1536/c))/4)*rot2x1[(rota[i][j]*rot2[i][j])%16])/25)+v*ran[i][j], 108+int((864*i)/r)+int(int(864/r)/2)+int((int(min(int(864/r), int(1536/c))/4)*rot2y1[(rota[i][j]*rot2[i][j])%16])/25)), int(min(int(864/r), int(1536/c))/4))
                    pygame.draw.circle(disWin, green, (192+int((1536*j)/c)+int(int(1536/c)/2)+int((int(min(int(864/r), int(1536/c))/4)*rot2x2[(rota[i][j]*rot2[i][j])%16])/25)+v*ran[i][j], 108+int((864*i)/r)+int(int(864/r)/2)+int((int(min(int(864/r), int(1536/c))/4)*rot2y2[(rota[i][j]*rot2[i][j])%16])/25)), int(min(int(864/r), int(1536/c))/4))
                elif(arr[i][j]==3):
                    pygame.draw.circle(disWin, red, (192+int((1536*j)/c)+int(int(1536/c)/2)+int((rot3x1[(rota[i][j]*rot3[i][j])%24]*int(min(int(864/r), int(1536/c))/4))/25)+v*ran[i][j], 108+int((864*i)/r)+int(int(864/r)/2)+int((rot3y1[(rota[i][j]*rot3[i][j])%24]*int(min(int(864/r), int(1536/c))/4))/25)), int(min(int(864/r), int(1536/c))/4))
                    pygame.draw.circle(disWin, red, (192+int((1536*j)/c)+int(int(1536/c)/2)+int((rot3x2[(rota[i][j]*rot3[i][j])%24]*int(min(int(864/r), int(1536/c))/4))/25)+v*ran[i][j], 108+int((864*i)/r)+int(int(864/r)/2)+int((rot3y2[(rota[i][j]*rot3[i][j])%24]*int(min(int(864/r), int(1536/c))/4))/25)), int(min(int(864/r), int(1536/c))/4))
                    pygame.draw.circle(disWin, red, (192+int((1536*j)/c)+int(int(1536/c)/2)+int((rot3x3[(rota[i][j]*rot3[i][j])%24]*int(min(int(864/r), int(1536/c))/4))/25)+v*ran[i][j], 108+int((864*i)/r)+int(int(864/r)/2)+int((rot3y3[(rota[i][j]*rot3[i][j])%24]*int(min(int(864/r), int(1536/c))/4))/25)), int(min(int(864/r), int(1536/c))/4))
                elif(arr[i][j]==-3):
                    pygame.draw.circle(disWin, green, (192+int((1536*j)/c)+int(int(1536/c)/2)+int((rot3x1[(rota[i][j]*rot3[i][j])%24]*int(min(int(864/r), int(1536/c))/4))/25)+v*ran[i][j], 108+int((864*i)/r)+int(int(864/r)/2)+int((rot3y1[(rota[i][j]*rot3[i][j])%24]*int(min(int(864/r), int(1536/c))/4))/25)), int(min(int(864/r), int(1536/c))/4))
                    pygame.draw.circle(disWin, green, (192+int((1536*j)/c)+int(int(1536/c)/2)+int((rot3x2[(rota[i][j]*rot3[i][j])%24]*int(min(int(864/r), int(1536/c))/4))/25)+v*ran[i][j], 108+int((864*i)/r)+int(int(864/r)/2)+int((rot3y2[(rota[i][j]*rot3[i][j])%24]*int(min(int(864/r), int(1536/c))/4))/25)), int(min(int(864/r), int(1536/c))/4))
                    pygame.draw.circle(disWin, green, (192+int((1536*j)/c)+int(int(1536/c)/2)+int((rot3x3[(rota[i][j]*rot3[i][j])%24]*int(min(int(864/r), int(1536/c))/4))/25)+v*ran[i][j], 108+int((864*i)/r)+int(int(864/r)/2)+int((rot3y3[(rota[i][j]*rot3[i][j])%24]*int(min(int(864/r), int(1536/c))/4))/25)), int(min(int(864/r), int(1536/c))/4))
    else:
        for i in range(0, r):
            for j in range(0, c):
                if(arr[i][j]==1):
                    pygame.draw.circle(disWin, red, (int((a*j)/c)+int(int(a/c)/2)+v*ran[i][j], int((b*i)/r)+int(int(b/r)/2)), int(min(int(b/r), int(a/c))/4))
                elif(arr[i][j]==-1):
                    pygame.draw.circle(disWin, green, (int((a*j)/c)+int(int(a/c)/2)+v*ran[i][j], int((b*i)/r)+int(int(b/r)/2)), int(min(int(b/r), int(a/c))/4))
                elif(arr[i][j]==2):
                    pygame.draw.circle(disWin, red, (int((a*j)/c)+int(int(a/c)/2)+int((rot2x1[(rota[i][j]*rot2[i][j])%16]*int(min(int(b/r), int(a/c))/4))/25)+v*ran[i][j], int((b*i)/r)+int(int(b/r)/2)+int((rot2y1[(rota[i][j]*rot2[i][j])%16]*int(min(int(b/r), int(a/c))/4))/25)), int(min(int(b/r), int(a/c))/4))
                    pygame.draw.circle(disWin, red, (int((a*j)/c)+int(int(a/c)/2)+int((rot2x2[(rota[i][j]*rot2[i][j])%16]*int(min(int(b/r), int(a/c))/4))/25)+v*ran[i][j], int((b*i)/r)+int(int(b/r)/2)+int((rot2y2[(rota[i][j]*rot2[i][j])%16]*int(min(int(b/r), int(a/c))/4))/25)), int(min(int(b/r), int(a/c))/4))
                elif(arr[i][j]==-2):
                    pygame.draw.circle(disWin, green, (int((a*j)/c)+int(int(a/c)/2)+int((rot2x1[(rota[i][j]*rot2[i][j])%16]*int(min(int(b/r), int(a/c))/4))/25)+v*ran[i][j], int((b*i)/r)+int(int(b/r)/2)+int((rot2y1[(rota[i][j]*rot2[i][j])%16]*int(min(int(b/r), int(a/c))/4))/25)), int(min(int(b/r), int(a/c))/4))
                    pygame.draw.circle(disWin, green, (int((a*j)/c)+int(int(a/c)/2)+int((rot2x2[(rota[i][j]*rot2[i][j])%16]*int(min(int(b/r), int(a/c))/4))/25)+v*ran[i][j], int((b*i)/r)+int(int(b/r)/2)+int((rot2y2[(rota[i][j]*rot2[i][j])%16]*int(min(int(b/r), int(a/c))/4))/25)), int(min(int(b/r), int(a/c))/4))
                elif(arr[i][j]==3):
                    pygame.draw.circle(disWin, red, (int((a*j)/c)+int(int(a/c)/2)+int((rot3x1[(rota[i][j]*rot3[i][j])%24]*int(min(int(b/r), int(a/c))/4))/25)+v*ran[i][j], int((b*i)/r)+int(int(b/r)/2)+int((rot3y1[(rota[i][j]*rot3[i][j])%24]*int(min(int(b/r), int(a/c))/4))/25)), int(min(int(b/r), int(a/c))/4))
                    pygame.draw.circle(disWin, red, (int((a*j)/c)+int(int(a/c)/2)+int((rot3x2[(rota[i][j]*rot3[i][j])%24]*int(min(int(b/r), int(a/c))/4))/25)+v*ran[i][j], int((b*i)/r)+int(int(b/r)/2)+int((rot3y2[(rota[i][j]*rot3[i][j])%24]*int(min(int(b/r), int(a/c))/4))/25)), int(min(int(b/r), int(a/c))/4))
                    pygame.draw.circle(disWin, red, (int((a*j)/c)+int(int(a/c)/2)+int((rot3x3[(rota[i][j]*rot3[i][j])%24]*int(min(int(b/r), int(a/c))/4))/25)+v*ran[i][j], int((b*i)/r)+int(int(b/r)/2)+int((rot3y3[(rota[i][j]*rot3[i][j])%24]*int(min(int(b/r), int(a/c))/4))/25)), int(min(int(b/r), int(a/c))/4))
                elif(arr[i][j]==-3):
                    pygame.draw.circle(disWin, green, (int((a*j)/c)+int(int(a/c)/2)+int((rot3x1[(rota[i][j]*rot3[i][j])%24]*int(min(int(b/r), int(a/c))/4))/25)+v*ran[i][j], int((b*i)/r)+int(int(b/r)/2)+int((rot3y1[(rota[i][j]*rot3[i][j])%24]*int(min(int(b/r), int(a/c))/4))/25)), int(min(int(b/r), int(a/c))/4))
                    pygame.draw.circle(disWin, green, (int((a*j)/c)+int(int(a/c)/2)+int((rot3x2[(rota[i][j]*rot3[i][j])%24]*int(min(int(b/r), int(a/c))/4))/25)+v*ran[i][j], int((b*i)/r)+int(int(b/r)/2)+int((rot3y2[(rota[i][j]*rot3[i][j])%24]*int(min(int(b/r), int(a/c))/4))/25)), int(min(int(b/r), int(a/c))/4))
                    pygame.draw.circle(disWin, green, (int((a*j)/c)+int(int(a/c)/2)+int((rot3x3[(rota[i][j]*rot3[i][j])%24]*int(min(int(b/r), int(a/c))/4))/25)+v*ran[i][j], int((b*i)/r)+int(int(b/r)/2)+int((rot3y3[(rota[i][j]*rot3[i][j])%24]*int(min(int(b/r), int(a/c))/4))/25)), int(min(int(b/r), int(a/c))/4))

def ident(i, j):
    if i==0 and j==0:
        return "topleft"
    elif i==0 and j==c-1:
        return "topright"
    elif i==r-1 and j==0:
        return "bottomleft"
    elif i==r-1 and j==c-1:
        return "bottomright"
    elif i==0 and (j>0 and j<c-1):
        return "top"
    elif i==r-1 and (j>0 and j<c-1):
        return "bottom"
    elif j==0 and (i>0 and i<r-1):
        return "left"
    elif j==c-1 and (i>0 and i<r-1):
        return "right"
    else:
        return "center"

def rxxn(ii, jj, s):
    arr[ii][jj]=(abs(arr[ii][jj])+1)*s
    rxn(ii, jj)

def rxn(i, j):
    iden=ident(i, j)
    sgn=(arr[i][j]/abs(arr[i][j]))
    if iden=="topleft" and (arr[i][j]==2 or arr[i][j]==-2):
        arr[i][j]=0
        rxxn(i, j+1, sgn)
        rxxn(i+1, j, sgn)
    elif iden=="topright" and (arr[i][j]==2 or arr[i][j]==-2):
        arr[i][j]=0
        rxxn(i, j-1, sgn)
        rxxn(i+1, j, sgn)
    elif iden=="bottomleft" and (arr[i][j]==2 or arr[i][j]==-2):
        arr[i][j]=0
        rxxn(i-1, j, sgn)
        rxxn(i, j+1, sgn)
    elif iden=="bottomright" and (arr[i][j]==2 or arr[i][j]==-2):
        arr[i][j]=0
        rxxn(i-1, j, sgn)
        rxxn(i, j-1, sgn)
    elif iden=="top" and (arr[i][j]==3 or arr[i][j]==-3):
        arr[i][j]=0
        rxxn(i, j-1, sgn)
        rxxn(i, j+1, sgn)
        rxxn(i+1, j, sgn)
    elif iden=="bottom" and (arr[i][j]==3 or arr[i][j]==-3):
        arr[i][j]=0
        rxxn(i-1, j, sgn)
        rxxn(i, j-1, sgn)
        rxxn(i, j+1, sgn)
    elif iden=="left" and (arr[i][j]==3 or arr[i][j]==-3):
        arr[i][j]=0
        rxxn(i-1, j, sgn)
        rxxn(i, j+1, sgn)
        rxxn(i+1, j, sgn)
    elif iden=="right" and (arr[i][j]==3 or arr[i][j]==-3):
        arr[i][j]=0
        rxxn(i-1, j, sgn)
        rxxn(i, j-1, sgn)
        rxxn(i+1, j, sgn)
    elif iden=="center" and (arr[i][j]==4 or arr[i][j]==-4):
        arr[i][j]=0
        rxxn(i-1, j, sgn)
        rxxn(i, j-1, sgn)
        rxxn(i, j+1, sgn)
        rxxn(i+1, j, sgn)

def victor(a, b, f):
    no=0
    nr=0
    ng=0
    for i in range(0, r):
        for j in range(0, c):
            if(arr[i][j]>0):
                nr+=1
            elif(arr[i][j]==0):
                no+=1
            else:
                ng+=1
    if(no<=r*c-2):
        if(nr==0):
            mssg = f.render("Green Wins!", True, green, black)
            mssgrect=mssg.get_rect()
            mssgrect.center=int(a/2), int(b/2)
            disWin.blit(mssg, mssgrect)
        elif(ng==0):
            mssg = f.render("Red Wins!", True, red, black)
            mssgrect=mssg.get_rect()
            mssgrect.center=int(a/2), int(b/2)
            disWin.blit(mssg, mssgrect)

def distex(f, text, col, a, b, x, y, mode):
    if mode:
        a=1536
        b=864
        tex=f.render(text, True, col)
        texrect=tex.get_rect()
        texrect.center=192+int(a*x), 108+int(b*y)
        disWin.blit(tex, texrect)
        i, j=texrect.topleft
        k, l=texrect.bottomright
        return i, j , k, l
    else:
        tex=f.render(text, True, col)
        texrect=tex.get_rect()
        texrect.center=int(a*x), int(b*y)
        disWin.blit(tex, texrect)
        i, j=texrect.topleft
        k, l=texrect.bottomright
        return i, j , k, l

while not gameExit:
    if state==0:
        cw, ch=pygame.display.get_surface().get_size()
        font = pygame.font.SysFont("comicsansms", int(min(cw, ch)/7))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True

            if event.type == pygame.VIDEORESIZE:
                if not fullscreen:
                    dis(event.w, event.h, pygame.RESIZABLE)

            if  event.type == pygame.KEYDOWN:
                if event.key == K_f:
                    fullscreen = not fullscreen
                    if fullscreen:
                        dis(monw, monh, pygame.FULLSCREEN)
                    else:
                        dis(dw, dh, pygame.RESIZABLE)

            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my=pygame.mouse.get_pos()
                if((mx>=p1 and mx<=p3) and (my>=p2 and my<=p4)):
                    state=3
                elif((mx>=q1 and mx<=q3) and (my>=q2 and my<=q4)):
                    gameExit=True


        disWin.fill(black)
        distex(font, "Chain Reaction", blue, cw, ch, 0.5, 0.2, fullscreen)
        p1, p2, p3, p4=distex(font, "Play", blue, cw, ch, 0.25, 0.75, fullscreen)
        q1, q2, q3, q4=distex(font, "Quit", blue, cw, ch, 0.75, 0.75, fullscreen)
    elif state==1:
        cw, ch=pygame.display.get_surface().get_size()
        font = pygame.font.SysFont("comicsansms", int(min(cw, ch)/7))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True

            if event.type == pygame.VIDEORESIZE:
                if not fullscreen:
                    dis(event.w, event.h, pygame.RESIZABLE)

            if  event.type == pygame.KEYDOWN:
                if event.key == K_f:
                    fullscreen = not fullscreen
                    if fullscreen:
                        dis(monw, monh, pygame.FULLSCREEN)
                    else:
                        dis(dw, dh, pygame.RESIZABLE)
                if event.key == K_ESCAPE:
                    state=2

            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my=pygame.mouse.get_pos()
                cnt=move(mx, my, cw, ch, cnt, fullscreen)
            
        cw, ch=pygame.display.get_surface().get_size()
        disWin.fill(black)
        grid(r, c, cw, ch, player[cnt], fullscreen)
        viba=(viba+1)%6
        for i in range(0, r):
            for j in range(0, c):
                rot2[i][j]=(rot2[i][j]+1)%16
        for i in range(0, r):
            for j in range(0, c):
                rot3[i][j]=(rot3[i][j]+1)%24
        shmv(cw, ch, vib[viba], fullscreen)
        victor(cw, ch, font)
    elif state==2:
        cw, ch=pygame.display.get_surface().get_size()
        font = pygame.font.SysFont("comicsansms", int(min(cw, ch)/7))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True

            if event.type == pygame.VIDEORESIZE:
                if not fullscreen:
                    dis(event.w, event.h, pygame.RESIZABLE)

            if  event.type == pygame.KEYDOWN:
                if event.key == K_f:
                    fullscreen = not fullscreen
                    if fullscreen:
                        dis(monw, monh, pygame.FULLSCREEN)
                    else:
                        dis(dw, dh, pygame.RESIZABLE)

            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my=pygame.mouse.get_pos()
                if((mx>=rm1 and mx<=rm3) and (my>=rm2 and my<=rm4)):
                    state=1
                elif((mx>=re1 and mx<=re3) and (my>=re2 and my<=re4)):
                    state=3
                elif((mx>=mm1 and mx<=mm3) and (my>=mm2 and my<=mm4)):
                    arr = np.array([[0]*c]*r)
                    state=0
        
        disWin.fill(black)
        distex(font, "Chain Reaction", blue, cw, ch, 0.5, 0.1, fullscreen)
        rm1, rm2, rm3, rm4=distex(font, "Resume", blue, cw, ch, 0.5, 0.4, fullscreen)
        re1, re2, re3, re4=distex(font, "Restart", blue, cw, ch, 0.5, 0.6, fullscreen)
        mm1, mm2, mm3, mm4=distex(font, "Main Menu", blue, cw, ch, 0.5, 0.8, fullscreen)
    elif state==3:
        cw, ch=pygame.display.get_surface().get_size()
        font = pygame.font.SysFont("comicsansms", int(min(cw, ch)/7))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True

            if event.type == pygame.VIDEORESIZE:
                if not fullscreen:
                    dis(event.w, event.h, pygame.RESIZABLE)

            if  event.type == pygame.KEYDOWN:
                if event.key == K_f:
                    fullscreen = not fullscreen
                    if fullscreen:
                        dis(monw, monh, pygame.FULLSCREEN)
                    else:
                        dis(dw, dh, pygame.RESIZABLE)
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my=pygame.mouse.get_pos()
                if((mx>=fo1 and mx<=fo3) and (my>=fo2 and my<=fo4)):
                    r=5
                    c=8
                    ran=np.array([[0]*c]*r)
                    for i in range(0, r):
                        for j in range(0, c):
                            ran[i][j]=random.choice(abx)
                    rota=np.array([[0]*c]*r)
                    for i in range(0, r):
                        for j in range(0, c):
                            rota[i][j]=random.choice(abx)
                    rot2=np.array([[0]*c]*r)
                    for i in range(0, r):
                        for j in range(0, c):
                            rot2[i][j]=random.randint(0, 16)
                    rot3=np.array([[0]*c]*r)
                    arr = np.array([[0]*c]*r)
                    for i in range(0, r):
                        for j in range(0, c):
                            rot3[i][j]=random.randint(0, 24)
                    state=1
                elif((mx>=os1 and mx<=os3) and (my>=os2 and my<=os4)):               
                    r=10
                    c=16
                    ran=np.array([[0]*c]*r)
                    for i in range(0, r):
                        for j in range(0, c):
                            ran[i][j]=random.choice(abx)
                    rota=np.array([[0]*c]*r)
                    for i in range(0, r):
                        for j in range(0, c):
                            rota[i][j]=random.choice(abx)
                    rot2=np.array([[0]*c]*r)
                    for i in range(0, r):
                        for j in range(0, c):
                            rot2[i][j]=random.randint(0, 16)
                    rot3=np.array([[0]*c]*r)
                    arr = np.array([[0]*c]*r)
                    for i in range(0, r):
                        for j in range(0, c):
                            rot3[i][j]=random.randint(0, 24)
                    arr = np.array([[0]*c]*r)
                    state=1
        
        disWin.fill(black)
        distex(font, "Choose Size", blue, cw, ch, 0.5, 0.2, fullscreen)
        fo1, fo2, fo3, fo4=distex(font, "5 x 8", blue, cw, ch, 0.25, 0.75, fullscreen)
        os1, os2, os3, os4=distex(font, "10 x 16", blue, cw, ch, 0.75, 0.75, fullscreen)

    pygame.display.update()
    clock.tick(15)



pygame.quit()
quit()
