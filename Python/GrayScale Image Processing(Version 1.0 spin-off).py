from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import *
from tkinter.simpledialog import *
import math
import math as m
import os.path


### 함수부
#******************
# 공통 함수부
#******************
def closeWindow():
    result = messagebox.askokcancel("종료", "프로그램을 종료하시겠습니까?")
    if result:
        window.quit()

def malloc2D(h, w, initValue=0) :
    memory = [ [initValue for _ in range(w)] for _ in range(h)]
    return memory

def openImage() :
    global window, canvas, paper, fullname
    global inImage, outImage, inH, inW, outH, outW
    fullname = askopenfilename(parent=window, filetypes=(('RAW파일', '*.raw'), ('모든파일', '*.*')))
    # 중요! 입력 이미지 크기를 결정
    fsize = os.path.getsize(fullname) # 파일 크기 (byte)
    inH= inW = int(math.sqrt(fsize))
    # 메모리 할당
    inImage = malloc2D(inH, inW)
    # 파일 --> 메모리
    rfp = open(fullname, 'rb')
    for i in range(inH):
        for k in range(inW):
            inImage[i][k] = ord(rfp.read(1))
    rfp.close()
    equalImage()

def saveImage():
    global window, canvas, paper, fullname
    global inImage, outImage, inH, inW, outH, outW
    if (outImage==None or len(outImage)==0): #영상처리를 한적이 없다면...
        messagebox.showerror('ERROR',' 저장 실패!')
        return
    wfp = asksaveasfile(parent=window, mode='wb',defaultextension='*.raw',
                        filetypes=(('RAW파일', '*.raw'), ('모든파일', '*.*')) )
    import struct
    for i in range(outH) :
        for k in range(outW) :
            wfp.write(struct.pack('B',outImage[i][k]) )
    wfp.close()
    messagebox.showinfo('SUCCESS',wfp.name + '에 저장 완료!')

def displayImage():
    global window, canvas, paper, fullname
    global inImage, outImage, inH, inW, outH, outW
    ## 기존에 이미지를 오픈한적이 있으면, 캔버스 뜯어내기
    if( canvas !=None):
        canvas.destroy()

    #벽, 캔버스, 종이 설정
    window.geometry(str(outH)+'x'+str(outW)) # "512x512"
    canvas = Canvas(window, height=outH, width=outW, bg='yellow')  # 칠판
    paper = PhotoImage(height=outH, width=outW)  # 종이
    canvas.create_image((outH // 2, outW // 2), image=paper, state='normal')
    ##메모리 --> 화면
    # for i in range(inH):
    #     for k in range(inW):
    #         r = g = b = outImage[i][k]
    #         paper.put('#%02x%02x%02x' % (r, g, b), (k, i))

    # 더블 버퍼링... 비슷한 기법(모두다 메모리상에 출력형태로 생성한 후에, 한방에 출력)
    rgbString=""
    for i in range(outH):
        oneString=""#한줄에 대한 16진수 문자열
        for k in range(outW):
            r = g = b = outImage[i][k]
            oneString += '#%02x%02x%02x ' % (r, g, b)
        rgbString += '{'+oneString+'} '
    paper.put(rgbString)

    canvas.pack()

#******************
# 영상처리 함수부
#******************
##화소점 처리
def equalImage(): #동일 이미지
    global window, canvas, paper, fullname
    global inImage, outImage, inH, inW, outH, outW
    # 중요! 출력 영상 크기 결정 --> 알고리즘에 의존
    outH = inH
    outW = inW
    # 메모리 할당
    outImage = malloc2D(outH,outW)
    ###진짜 영상처리 알고리즘###
    for i in range(inH):
        for k in range(inW):
            outImage[i][k]=inImage[i][k]
    ###########################
    displayImage()

def addImage(): #밝게/어둡게 이미지
    global window, canvas, paper, fullname
    global inImage, outImage, inH, inW, outH, outW
    # 중요! 출력 영상 크기 결정 --> 알고리즘에 의존
    outH = inH
    outW = inW
    # 메모리 할당
    outImage = malloc2D(outH,outW)
    ###진짜 영상처리 알고리즘###
    value=0
    value=askinteger("정수 입력",'-255~255 입력', maxvalue=255,minvalue=-255)
    for i in range(inH):
        for k in range(inW):
            outImage[i][k] = inImage[i][k] + value
            if(outImage[i][k] > 255) :
                outImage[i][k]=255
            if(outImage[i][k] < 0) :
                outImage[i][k]=0
    ###########################
    displayImage()

def reverseImage(): #반전 이미지
    global window, canvas, paper, fullname
    global inImage, outImage, inH, inW, outH, outW
    # 중요! 출력 영상 크기 결정 --> 알고리즘에 의존
    outH = inH
    outW = inW
    # 메모리 할당
    outImage = malloc2D(outH,outW)
    ###진짜 영상처리 알고리즘###
    for i in range(inH):
        for k in range(inW):
            outImage[i][k]=255-inImage[i][k]
    ###########################
    displayImage()

def bwImage(): #흑백 이미지
    global window, canvas, paper, fullname
    global inImage, outImage, inH, inW, outH, outW
    # 중요! 출력 영상 크기 결정 --> 알고리즘에 의존
    outH = inH
    outW = inW
    # 메모리 할당
    outImage = malloc2D(outH,outW)
    ###진짜 영상처리 알고리즘###
    for i in range(inH):
        for k in range(inW):
            if (inImage[i][k] > 127):
                outImage[i][k] = 255
            else:
                outImage[i][k] = 0
    ###########################
    displayImage()

def gamma(): #감마 이미지
    global window, canvas, paper, fullname
    global inImage, outImage, inH, inW, outH, outW
    # 중요! 출력 영상 크기 결정 --> 알고리즘에 의존
    outH = inH
    outW = inW
    # 메모리 할당
    outImage = malloc2D(outH,outW)
    ###진짜 영상처리 알고리즘###
    gamma=0
    gamma = askfloat("감마보정", "감마보정 할 값을 입력하세요.", minvalue=0, maxvalue=3)
    for i in range(inH):
        for k in range(inW):
            outImage[i][k] = int(255.0 * ((float(inImage[i][k]) / 255.0) ** gamma))

    ###########################
    displayImage()


def para1Image(): #파라볼라(CAP) 이미지
    global window, canvas, paper, fullname
    global inImage, outImage, inH, inW, outH, outW
    # 중요! 출력 영상 크기 결정 --> 알고리즘에 의존
    outH = inH
    outW = inW
    # 메모리 할당
    outImage = malloc2D(outH,outW)
    ###진짜 영상처리 알고리즘###
    # Output = 255*((Input/127)-1)^2
    for i in range(inH):
        for k in range(inW):
            m = inImage[i][k]
            outImage[i][k] = int(255. * math.pow((m / 127.) - 1, 2))
    ###########################
    displayImage()

def para2Image(): #파라볼라(CUP) 이미지
    global window, canvas, paper, fullname
    global inImage, outImage, inH, inW, outH, outW
    # 중요! 출력 영상 크기 결정 --> 알고리즘에 의존
    outH = inH
    outW = inW
    # 메모리 할당
    outImage = malloc2D(outH,outW)
    ###진짜 영상처리 알고리즘###
    # Output = -255*((Input/127)-1)^2 +255
    for i in range(inH):
        for k in range(inW):
            m = inImage[i][k]
            outImage[i][k] =int(255. - 255 * math.pow((m / 127.) - 1, 2))
    displayImage()

## 기하학 처리
def zoomOut(): #축소
    global window, canvas, paper, fullname
    global inImage, outImage, inH, inW, outH, outW
    value = 0
    value = askinteger("축소", "축소 할 값을 입력하세요.", minvalue=-255, maxvalue=255)
    outH = int(inH / value)
    outW = int(inW / value)
    # 출력 이미지 메모리 확보
    outImage = malloc2D(outH, outW)
    ### 진짜 영상처리 알고리즘 ##
    for i in range(inH):
        for k in range(inW):
            outImage[int(i/value)][int(k/value)] = inImage[i][k]
    #############################
    displayImage()

def zoomin(): #확대
    global window, canvas, paper, fullname
    global inImage, outImage, inH, inW, outH, outW
    value = 0
    value = askinteger("확대", "확대 할 값을 입력하세요.", minvalue=-255, maxvalue=255)
    outH = int(inH * value)
    outW = int(inW * value)
    # 출력 이미지 메모리 확보
    outImage = malloc2D(outH, outW)
    ### 진짜 영상처리 알고리즘 ##
    for i in range(inH):
        for k in range(inW):
            outImage[int(i*value)][int(k*value)] = inImage[i][k]
    #############################
    displayImage()

def zoomin2(): #확대2
    global window, canvas, paper, fullname
    global inImage, outImage, inH, inW, outH, outW
    value = 0
    value = askinteger("확대", "확대 할 값을 입력하세요.", minvalue=-255, maxvalue=255)
    outH = int(inH * value)
    outW = int(inW * value)
    # 출력 이미지 메모리 확보
    outImage = malloc2D(outH, outW)
    ### 진짜 영상처리 알고리즘 ##
    for i in range(outH):
        for k in range(outW):
            outImage[i][k] = inImage[(int)(i / value)][(int)(k / value)]
    #############################
    displayImage()

def rotateImage(): #회전
    global window, canvas, paper, fullname
    global inImage, outImage, inH, inW, outH, outW

    outH = inH
    outW = inW
    outImage = malloc2D(outH,outW)
    degree = 0
    radian = 0
    degree = askinteger("회전", "회전할 값을 입력하세요.", minvalue=-360, maxvalue=360)
    radian = degree * math.pi / 180.0
    ###진짜 영상처리 알고리즘###
    for i in range(inH):
        for k in range(inW):
            xs = i
            ys = k
            xd = (int)(math.cos(radian) * xs - math.sin(radian) * ys)
            yd = (int)(math.sin(radian) * xs + math.cos(radian) * ys)
            if ((0 <= xd < outH) & (0 <= yd < outW)):
                outImage[xd][yd] = inImage[xs][ys]
    ###########################
    displayImage()

def rotateImage2(): #회전2
    global window, canvas, paper, fullname
    global inImage, outImage, inH, inW, outH, outW
    outH = inH
    outW = inW
    outImage = malloc2D(outH,outW)
    degree = 0
    radian = 0
    degree = askinteger("회전", "회전할 값을 입력하세요.", minvalue=-360, maxvalue=360)
    radian = degree * math.pi / 180.0
    cx = inH // 2
    cy = inW // 2
    ###진짜 영상처리 알고리즘###
    for i in range(outH):
        for k in range(outW):
            xd = i
            yd = k
            xs = int(math.cos(radian) * (xd - cx) + math.sin(radian) * (yd - cy)) + cx
            ys = int(-math.sin(radian) * (xd - cx) + math.cos(radian) * (yd - cy)) + cy
            if (0 <= xs < outH) and (0 <= ys < outW):
                outImage[xd][yd] = inImage[xs][ys]
    ###########################
    displayImage()

def moveImage() :
    global inImage, outImage, inH, inW, outH, outW, move_x, move_y
    global window, canvas, paper
    outH = inH
    outW = inW
    outImage = malloc2D(outH, outW)

    ## 진짜 영상처리 알고리즘 ##
    move_x, move_y = 0, 0
    value1 = askinteger("이동(x축)", "움직일 x축 값을 입력하세요.", minvalue=-inW, maxvalue=inW)
    value2 = askinteger("이동(y축)", "움직일 y값을 입력하세요.", minvalue=-inH, maxvalue=inH)
    for i in range(inH):
        for k in range(inW):
            outImage[i][k] = 0

    for i in range(inH):
        for k in range(inW):
            move_x = i - int(value1)
            move_y = k + int(value2)
            if ((0 <= move_x and move_x < inH) and (0 <= move_y and move_y < inW)):
                outImage[move_x][move_y] = inImage[i][k]
    displayImage()

def RightLeftMirror(): #좌우반전
    global window, canvas, paper, fullname
    global inImage, outImage, inH, inW, outH, outW
    outH = inH
    outW = inW
    outImage = malloc2D(outH, outW)
    ###진짜 영상처리 알고리즘###
    for i in range(inH):
        for k in range(inW):
            outImage[i][(inW - 1) - k] = inImage[i][k]
    ###########################
    displayImage()

def UpDownMirror(): #상하반전
    global window, canvas, paper, fullname
    global inImage, outImage, inH, inW, outH, outW
    outH = inH
    outW = inW
    outImage = malloc2D(outH, outW)
    ###진짜 영상처리 알고리즘###
    for i in range(inH):
        for k in range(inW):
            outImage[(inH - 1) - i][k] = inImage[i][k]
    ###########################
    displayImage()

def UpDownRightLeftMirror(): #상하반전
    global window, canvas, paper, fullname
    global inImage, outImage, inH, inW, outH, outW
    outH = inH
    outW = inW
    outImage = malloc2D(outH, outW)
    ###진짜 영상처리 알고리즘###
    for i in range(inH):
        for k in range(inW):
            outImage[(inH - 1) - i][(inW - 1) - k] = inImage[i][k]
    ###########################
    displayImage()

def histoStretch(): #히스토그램 스트래칭
    global window, canvas, paper, fullname
    global inImage, outImage, inH, inW, outH, outW
    outH = inH
    outW = inW
    outImage = malloc2D(outH,outW)
    ###진짜 영상처리 알고리즘###
    # new = (old - low) / (high - low) * 255.0
    high = inImage[0][0]
    low = inImage[0][0]
    for i in range(inH):
        for k in range(inW):
            if (inImage[i][k] < low):
                low = inImage[i][k]
            if (inImage[i][k] > high):
                high = inImage[i][k]
    old , new = 0, 0
    for i in range(inH):
        for k in range(inW):
            old=inImage[i][k]
            new = (int)((old - low) / (high - low) * 255.0)
            if (new > 255):
                new = 255
            if (new < 0):
                new = 0
            outImage[i][k] = new
    ###########################
    displayImage()

def endIn(): #엔드-인 탐색
    global window, canvas, paper, fullname
    global inImage, outImage, inH, inW, outH, outW
    outH = inH
    outW = inW
    outImage = malloc2D(outH,outW)
    ###진짜 영상처리 알고리즘###
    high = inImage[0][0]
    low = inImage[0][0]
    for i in range(inH):
        for k in range(inW):
            if (inImage[i][k] < low):
                low = inImage[i][k]
            if (inImage[i][k] > high):
                high = inImage[i][k]
    high = high-50
    low = low+50
    old , new = 0, 0
    for i in range(inH):
        for k in range(inW):
            old=inImage[i][k]
            new = (int)((old - low) / (high - low) * 255.0)
            if (new > 255):
                new = 255
            if (new < 0):
                new = 0
            outImage[i][k] = new
    ###########################
    displayImage()

def histoEqual(): #평활화
    global window, canvas, paper, fullname
    global inImage, outImage, inH, inW, outH, outW
    outH = inH
    outW = inW
    outImage = malloc2D(outH,outW)
    ###진짜 영상처리 알고리즘###
    ## 1단계 : 히스토그램 생성 ##
    histo = []
    histo = [0 for _ in range(256)]
    for i in range(inH):
        for k in range(inW):
            histo[inImage[i][k]] += 1
    ## 2단계 : 누적 히스토그램 생성
    sumhisto = []
    sumhisto = [0 for _ in range(256)]
    for i in range(256):
        sumhisto[i] = sumhisto[i - 1] + histo[i]
    ## 3단계 : 정규화된 누적 히스토그램
    ## n = sum * ( 1 / (inH * inW) ) * 255
    nomalhisto = [0 for _ in range(256)]
    for i in range(256):
        nomalhisto[i] = int(sumhisto[i] * (1.0 / (inH * inW)) * 255.0)
    ## 4단계 : 원래값을 정규화 값으로 치환
    for i in range(inH):
        for k in range(inW):
            outImage[i][k] = nomalhisto[inImage[i][k]]
    ###########################
    displayImage()

def Emboss():
    global window, canvas, paper, fullname
    global inImage, outImage, inH, inW, outH, outW
    outH = inH
    outW = inW
    outImage = malloc2D(outH,outW)
    ###진짜 영상처리 알고리즘###
    MSIZE = 3
    mask = [[-1, 0, 0],
            [ 0, 0, 0],
            [ 0, 0, 1]] #엠보싱 마스크
    #임시 메모리 할당
    tmpInImage = malloc2D(inH + 2, inW + 2)
    tmpOutImage = malloc2D(outH, outW)

    # 입력 영상 --> 임시 입력 영상
    for i in range(inH):
        for k in range(inW):
            tmpInImage[i + 1][k + 1] = inImage[i][k]
    # 회선 연산
    for i in range(inH):
        for k in range(inW):
            SR = 0
            for m in range(MSIZE):
                for n in range(MSIZE):
                    SR += int(tmpInImage[i + m][k + n] * mask[m][n])
            tmpOutImage[i][k] = SR
    # 후처리 (마스크 합계에 따라서)
    for i in range(outH):
        for k in range(outW):
            tmpOutImage[i][k] += 127

    # 임시 출력 --> 출력 메모리
    for i in range(outH):
        for k in range(outW):
            if (tmpOutImage[i][k] > 255):
                tmpOutImage[i][k] = 255
            elif (tmpOutImage[i][k] < 0):
                tmpOutImage[i][k] = 0
            outImage[i][k] = tmpOutImage[i][k]
    displayImage()

def Blur():
    global window, canvas, paper, fullname
    global inImage, outImage, inH, inW, outH, outW
    outH = inH
    outW = inW
    outImage = malloc2D(outH,outW)
    ###진짜 영상처리 알고리즘###
    MSIZE = 3
    mask = [[1 / 9, 1 / 9, 1 / 9],
            [1 / 9, 1 / 9, 1 / 9],
            [1 / 9, 1 / 9, 1 / 9]] #블러링 마스크
    #임시 메모리 할당
    tmpInImage = malloc2D(inH + 2, inW + 2)
    tmpOutImage = malloc2D(outH, outW)

    # 입력 영상 --> 임시 입력 영상
    for i in range(inH):
        for k in range(inW):
            tmpInImage[i + 1][k + 1] = inImage[i][k]
    # 회선 연산
    for i in range(inH):
        for k in range(inW):
            SR = 0
            for m in range(MSIZE):
                for n in range(MSIZE):
                    SR += int(tmpInImage[i + m][k + n] * mask[m][n])
            tmpOutImage[i][k] = SR

    # 임시 출력 --> 출력 메모리
    for i in range(outH):
        for k in range(outW):
            if (tmpOutImage[i][k] > 255):
                tmpOutImage[i][k] = 255
            elif (tmpOutImage[i][k] < 0):
                tmpOutImage[i][k] = 0
            outImage[i][k] = tmpOutImage[i][k]
    displayImage()

def Sharp():
    global window, canvas, paper, fullname
    global inImage, outImage, inH, inW, outH, outW
    outH = inH
    outW = inW
    outImage = malloc2D(outH,outW)
    ###진짜 영상처리 알고리즘###
    MSIZE = 3
    mask = [[-1, -1, -1],
            [-1,  9, -1],
            [-1, -1, -1]] # 샤프닝 마스크
    #임시 메모리 할당
    tmpInImage = malloc2D(inH + 2, inW + 2)
    tmpOutImage = malloc2D(outH, outW)

    # 입력 영상 --> 임시 입력 영상
    for i in range(inH):
        for k in range(inW):
            tmpInImage[i + 1][k + 1] = inImage[i][k]
    # 회선 연산
    for i in range(inH):
        for k in range(inW):
            SR = 0
            for m in range(MSIZE):
                for n in range(MSIZE):
                    SR += int(tmpInImage[i + m][k + n] * mask[m][n])
            tmpOutImage[i][k] = SR

    # 임시 출력 --> 출력 메모리
    for i in range(outH):
        for k in range(outW):
            if (tmpOutImage[i][k] > 255):
                tmpOutImage[i][k] = 255
            elif (tmpOutImage[i][k] < 0):
                tmpOutImage[i][k] = 0
            outImage[i][k] = tmpOutImage[i][k]
    displayImage()


def Edge():
    global window, canvas, paper, fullname
    global inImage, outImage, inH, inW, outH, outW
    outH = inH
    outW = inW
    outImage = malloc2D(outH,outW)
    ###진짜 영상처리 알고리즘###
    MSIZE = 3
    mask = [[-1, 0,-1],
            [ 0, 2, 0],
            [ 0, 0, 0]]  # 엣지 마스크
    #임시 메모리 할당
    tmpInImage = malloc2D(inH + 2, inW + 2)
    tmpOutImage = malloc2D(outH, outW)

    # 입력 영상 --> 임시 입력 영상
    for i in range(inH):
        for k in range(inW):
            tmpInImage[i + 1][k + 1] = inImage[i][k]
    # 회선 연산
    for i in range(inH):
        for k in range(inW):
            SR = 0
            for m in range(MSIZE):
                for n in range(MSIZE):
                    SR += int(tmpInImage[i + m][k + n] * mask[m][n])
            tmpOutImage[i][k] = SR

    # 임시 출력 --> 출력 메모리
    for i in range(outH):
        for k in range(outW):
            if (tmpOutImage[i][k] > 255):
                tmpOutImage[i][k] = 255
            elif (tmpOutImage[i][k] < 0):
                tmpOutImage[i][k] = 0
            outImage[i][k] = tmpOutImage[i][k]
    displayImage()


### 전역 변수부
window, canvas, paper = None, None, None
inImage, outImage = [], []
inH, inW, outH, outW = [0]*4
fullname = ''


### 메인 코드부
window = Tk() # 벽
window.geometry("400x250")
window.resizable(width=False, height=False)
window.title("GrayScale Image Processing (Version 1.5)")

# 메뉴 만들기
mainMenu = Menu(window,) # 메뉴의 틀
window.config(menu=mainMenu)

# 상위 메뉴 (파일)
fileMenu = Menu(mainMenu,tearoff=0)
mainMenu.add_cascade(label='파일',menu=fileMenu)
fileMenu.add_command(label='열기',command=openImage)
fileMenu.add_command(label='저장',command=saveImage)
fileMenu.add_separator()
fileMenu.add_command(label='종료',command=closeWindow)

# 상위 메뉴 (화소점처리)
pixelMenu = Menu(mainMenu,tearoff=0)
mainMenu.add_cascade(label='화소점 처리', menu=pixelMenu)
paraMenu = Menu(pixelMenu,tearoff=0)
pixelMenu.add_command(label='동일 이미지', command=equalImage)
pixelMenu.add_command(label='밝게/어둡게', command=addImage)
pixelMenu.add_command(label='반전', command= reverseImage)
pixelMenu.add_command(label='흑백', command= bwImage)
pixelMenu.add_command(label='감마', command= gamma)

pixelMenu.add_cascade(label='파라볼라', menu=paraMenu)
paraMenu.configure(foreground='#4659E2', background='white')
paraMenu.add_command(label='CAP', command= para1Image)
paraMenu.add_command(label='CUP', command= para2Image)

# 상위 메뉴 (기하학처리)
pixelMenu2 = Menu(mainMenu,tearoff=0)
mainMenu.add_cascade(label='기하학 처리', menu=pixelMenu2)
mirrorMenu = Menu(pixelMenu2,tearoff=0)
zoomInMenu = Menu(pixelMenu2,tearoff=0)
rotateMenu = Menu(pixelMenu2,tearoff=0)

pixelMenu2.add_command(label='축소', command=zoomOut)
pixelMenu2.add_cascade(label='확대', menu=zoomInMenu) # 확대
zoomInMenu.configure(foreground='#4659E2', background='white')
zoomInMenu.add_command(label='포워딩', command=zoomin)
zoomInMenu.add_command(label='백워딩', command=zoomin2)

pixelMenu2.add_cascade(label='회전', menu=rotateMenu) # 회전
rotateMenu.configure(foreground='#4659E2', background='white')
rotateMenu.add_command(label='기본', command=rotateImage)
rotateMenu.add_command(label='중앙+백워딩', command=rotateImage2)

pixelMenu2.add_command(label='이동', command=moveImage)
pixelMenu2.add_cascade(label='미러링',menu=mirrorMenu) #미러링
mirrorMenu.configure(foreground='#4659E2', background='white')
mirrorMenu.add_command(label='좌우반전',command=RightLeftMirror)
mirrorMenu.add_command(label='상하반전',command=UpDownMirror)
mirrorMenu.add_command(label='상하좌우반전',command=UpDownRightLeftMirror)

# 상위 메뉴 (히스토그램)
pixelMenu3 = Menu(mainMenu,tearoff=0)
mainMenu.add_cascade(label='히스토그램', menu=pixelMenu3)
pixelMenu3.add_command(label='스트래칭', command=histoStretch)
pixelMenu3.add_command(label='엔드-인', command=endIn)
pixelMenu3.add_command(label='평활화', command=histoEqual)

# 상위 메뉴 (화소영역 처리)
pixelMenu4 = Menu(mainMenu,tearoff=0)
mainMenu.add_cascade(label='화소영역 처리', menu=pixelMenu4)
pixelMenu4.add_command(label='엠보싱', command=Emboss)
pixelMenu4.add_command(label='블러링', command=Blur)
pixelMenu4.add_command(label='샤프닝', command=Sharp)
pixelMenu4.add_command(label='경계선 검출', command=Edge)



window.mainloop()

