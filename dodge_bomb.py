import os
import sys
import random
import pygame as pg
import time


WIDTH, HEIGHT = 1600, 900
sum_mv_dic={   #移動量辞書（押下キー：移動量）
    pg.K_UP:(0,-5),
    pg.K_DOWN:(0,+5),
    pg.K_LEFT:(-5,0),
    pg.K_RIGHT:(+5,0)
}


os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(obj_rct:pg.Rect) -> tuple[bool,bool]:
    """
    こうかとんRect　または　爆弾Rectと画面内外判定用関数
    引数：こうかとんRect　または　爆弾Rect
    戻り値：横方向判定、縦方向判定（True画面内；False：画面外）
    """
    yoko,tate=True,True
    if obj_rct.left < 0 or WIDTH < obj_rct.right:
        yoko=False
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom:
        tate=False
    return yoko,tate


def game_over(): 
    """
    ゲームオーバーしたときに呼び出す関数
    背景が暗くなりGame Overと表示され
    泣いているこうかとんが表示される
    引数および戻り値はない
    """
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    ckk_img = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 2.0)  # 泣いているこうかとんの読み込み
    clock = pg.time.Clock()
    screen.blit(bg_img, [0, 0]) 
    kurai=pg.Surface((WIDTH,HEIGHT))
    kurai.set_alpha(200)
    screen.blit(kurai,[0,0])
    fonto = pg.font.Font(None,80)
    txt=fonto.render("Game Over",True,(255,255,255))
    screen.blit(txt,[WIDTH/2,HEIGHT/2])
    screen.blit(ckk_img, (WIDTH/2-150,HEIGHT/2-30))
    pg.display.update()
    clock.tick(1/5)


def kasoku():
    """
    時間経過で爆弾が加速する
    １０段階で加速する
    """
    acc = [a for a in range(1,11)]
    for r in range(1,11):
        bb_img=pg.Surface((20*r,20*r))
        pg.draw.circle(bb,(255,0,0),(10*r,10*r),10*r)


def main():  
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 2.0)
    ckk_img = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 2.0)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 900, 400
    clock = pg.time.Clock()
    tmr = 0
    bom_enn=pg.Surface((20,20))
    pg.draw.circle(bom_enn,(255,0,0),(10,10),10)
    bom_enn.set_colorkey((0,0,0))
    bom_rct=bom_enn.get_rect()
    bom_rct.center=random.randint(0,WIDTH),random.randint(0,HEIGHT)
    vx,vy=5,5


    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        if kk_rct.colliderect(bom_rct):
            game_over()
            return
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for k,v in sum_mv_dic.items():
            if key_lst[k]:
                sum_mv[0]+=v[0]
                sum_mv[1]+=v[1]
        
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct)!=(True,True):
            kk_rct.move_ip(-sum_mv[0],-sum_mv[1])
        screen.blit(kk_img, kk_rct)
        screen.blit(bom_enn,bom_rct)
        bom_rct.move_ip(vy,vx)
        yoko,tate=check_bound(bom_rct)
        if not tate:
            vx*=-1
        if not yoko:
            vy*=-1

        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
