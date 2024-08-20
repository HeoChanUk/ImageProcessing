
// ColorImageAlpha1View.cpp: CColorImageAlpha1View 클래스의 구현
//

#include "pch.h"
#include "framework.h"
// SHARED_HANDLERS는 미리 보기, 축소판 그림 및 검색 필터 처리기를 구현하는 ATL 프로젝트에서 정의할 수 있으며
// 해당 프로젝트와 문서 코드를 공유하도록 해 줍니다.
#ifndef SHARED_HANDLERS
#include "ColorImageAlpha1.h"
#endif

#include "ColorImageAlpha1Doc.h"
#include "ColorImageAlpha1View.h"

#ifdef _DEBUG
#define new DEBUG_NEW
#endif


// CColorImageAlpha1View

IMPLEMENT_DYNCREATE(CColorImageAlpha1View, CView)

BEGIN_MESSAGE_MAP(CColorImageAlpha1View, CView)
	// 표준 인쇄 명령입니다.
	ON_COMMAND(ID_FILE_PRINT, &CView::OnFilePrint)
	ON_COMMAND(ID_FILE_PRINT_DIRECT, &CView::OnFilePrint)
	ON_COMMAND(ID_FILE_PRINT_PREVIEW, &CView::OnFilePrintPreview)
	ON_COMMAND(IDM_EQUAL_IMAGE, &CColorImageAlpha1View::OnEqualImage)
	ON_COMMAND(IDM_GRAY_SCALE, &CColorImageAlpha1View::OnGrayScale)
	ON_COMMAND(IDM_ADD_IMAGE, &CColorImageAlpha1View::OnAddImage)
	ON_COMMAND(IDM_REVERSE_IMAGE, &CColorImageAlpha1View::OnReverseImage)
	ON_COMMAND(IDM_BW_IMAGE, &CColorImageAlpha1View::OnBwImage)
	ON_COMMAND(IDM_RGB_BW, &CColorImageAlpha1View::OnRgbBw)
	ON_COMMAND(IDM_GAMMA_IMAGE, &CColorImageAlpha1View::OnGammaImage)
	ON_COMMAND(IDM_CHANGE_SATUR, &CColorImageAlpha1View::OnChangeSatur)
	ON_COMMAND(IDM_PICK_ORANGE, &CColorImageAlpha1View::OnPickOrange)
END_MESSAGE_MAP()

// CColorImageAlpha1View 생성/소멸

CColorImageAlpha1View::CColorImageAlpha1View() noexcept
{
	// TODO: 여기에 생성 코드를 추가합니다.

}

CColorImageAlpha1View::~CColorImageAlpha1View()
{
}

BOOL CColorImageAlpha1View::PreCreateWindow(CREATESTRUCT& cs)
{
	// TODO: CREATESTRUCT cs를 수정하여 여기에서
	//  Window 클래스 또는 스타일을 수정합니다.

	return CView::PreCreateWindow(cs);
}

// CColorImageAlpha1View 그리기

void CColorImageAlpha1View::OnDraw(CDC* pDC)
{

	///////////////
	///////////////
	// 화면 크기 조절
	/////////////
	///////////////

	///////////////////
	/// ** 더블 버퍼링 **
	///////////////////
	CColorImageAlpha1Doc* pDoc = GetDocument();
	ASSERT_VALID(pDoc);
	if (!pDoc)
		return;

	/////////////////////
	/// 성능 개선을 위한 더블 버퍼링 
	////////////////////
	int i, k;
	unsigned char R, G, B;
	// 메모리 DC 선언
	CDC memDC;
	CBitmap* pOldBitmap, bitmap;

	// 화면 DC와 호환되는 메모리 DC 객체를 생성
	memDC.CreateCompatibleDC(pDC);

	// 마찬가지로 화면 DC와 호환되는 Bitmap 생성
	bitmap.CreateCompatibleBitmap(pDC, pDoc->m_inW, pDoc->m_inH);

	pOldBitmap = memDC.SelectObject(&bitmap);
	memDC.PatBlt(0, 0, pDoc->m_inW, pDoc->m_inH, WHITENESS); // 흰색으로 초기화


	// 출력 영상의 크기를 자동 조절
	double MAXSIZE = 800;  // 필요시 실 모니터 또는 화면의 해상도에 따라서 변경 가능!
	int inH = pDoc->m_inH;
	int inW = pDoc->m_inW;
	double hop = 1.0; // 기본

	if (inH > MAXSIZE || inW > MAXSIZE) {
		// hop을 새로 계산.
		if (inW > inH)
			hop = (inW / MAXSIZE);
		else
			hop = (inH / MAXSIZE);

		inW = (int)(inW / hop);
		inH = (int)(inH / hop);
	}

	// 메모리 DC에 그리기
	for (i = 0; i < inH; i++) {
		for (k = 0; k < inW; k++) {
			R = pDoc->m_inImageR[(int)(i * hop)][(int)(k * hop)];
			G = pDoc->m_inImageG[(int)(i * hop)][(int)(k * hop)];
			B = pDoc->m_inImageB[(int)(i * hop)][(int)(k * hop)];
			memDC.SetPixel(k, i, RGB(R, G, B));
		}
	}

	// 메모리 DC를 화면 DC에 고속 복사
	pDC->BitBlt(5, 5, pDoc->m_inW, pDoc->m_inH, &memDC, 0, 0, SRCCOPY);

	memDC.SelectObject(pOldBitmap);
	memDC.DeleteDC();
	bitmap.DeleteObject();

	///////////////////

	// 화면 DC와 호환되는 메모리 DC 객체를 생성
	memDC.CreateCompatibleDC(pDC);

	// 마찬가지로 화면 DC와 호환되는 Bitmap 생성
	bitmap.CreateCompatibleBitmap(pDC, pDoc->m_outW, pDoc->m_outH);

	pOldBitmap = memDC.SelectObject(&bitmap);
	memDC.PatBlt(0, 0, pDoc->m_outW, pDoc->m_outH, WHITENESS); // 흰색으로 초기화

	int outH = pDoc->m_outH;
	int outW = pDoc->m_outW;
	hop = 1.0; // 기본

	if (outH > MAXSIZE || outW > MAXSIZE) {
		// hop을 새로 계산.
		if (outW > outH)
			hop = (outW / MAXSIZE);
		else
			hop = (outH / MAXSIZE);

		outW = (int)(outW / hop);
		outH = (int)(outH / hop);
	}

	// 메모리 DC에 그리기
	for (i = 0; i < outH; i++) {
		for (k = 0; k < outW; k++) {
			R = pDoc->m_outImageR[(int)(i * hop)][(int)(k * hop)];
			G = pDoc->m_outImageG[(int)(i * hop)][(int)(k * hop)];
			B = pDoc->m_outImageB[(int)(i * hop)][(int)(k * hop)];
			memDC.SetPixel(k, i, RGB(R, G, B));
		}
	}
	// 메모리 DC를 화면 DC에 고속 복사
	pDC->BitBlt(inW + 10, 5, pDoc->m_outW, pDoc->m_outH, &memDC, 0, 0, SRCCOPY);

	memDC.SelectObject(pOldBitmap);
	memDC.DeleteDC();
	bitmap.DeleteObject();
}

// CColorImageAlpha1View 인쇄

BOOL CColorImageAlpha1View::OnPreparePrinting(CPrintInfo* pInfo)
{
	// 기본적인 준비
	return DoPreparePrinting(pInfo);
}

void CColorImageAlpha1View::OnBeginPrinting(CDC* /*pDC*/, CPrintInfo* /*pInfo*/)
{
	// TODO: 인쇄하기 전에 추가 초기화 작업을 추가합니다.
}

void CColorImageAlpha1View::OnEndPrinting(CDC* /*pDC*/, CPrintInfo* /*pInfo*/)
{
	// TODO: 인쇄 후 정리 작업을 추가합니다.
}


// CColorImageAlpha1View 진단

#ifdef _DEBUG
void CColorImageAlpha1View::AssertValid() const
{
	CView::AssertValid();
}

void CColorImageAlpha1View::Dump(CDumpContext& dc) const
{
	CView::Dump(dc);
}

CColorImageAlpha1Doc* CColorImageAlpha1View::GetDocument() const // 디버그되지 않은 버전은 인라인으로 지정됩니다.
{
	ASSERT(m_pDocument->IsKindOf(RUNTIME_CLASS(CColorImageAlpha1Doc)));
	return (CColorImageAlpha1Doc*)m_pDocument;
}
#endif //_DEBUG


// CColorImageAlpha1View 메시지 처리기



void CColorImageAlpha1View::OnEqualImage()
{
	// TODO: 여기에 명령 처리기 코드를 추가합니다.
	CColorImageAlpha1Doc* pDoc = GetDocument();
	ASSERT_VALID(pDoc);
	pDoc->OnEqualImage();
	Invalidate(TRUE);
}


void CColorImageAlpha1View::OnGrayScale()
{
	// TODO: 여기에 명령 처리기 코드를 추가합니다.
	CColorImageAlpha1Doc* pDoc = GetDocument();
	ASSERT_VALID(pDoc);
	pDoc->OnGrayScale();
	Invalidate(TRUE);
}


void CColorImageAlpha1View::OnAddImage()
{
	// TODO: 여기에 명령 처리기 코드를 추가합니다.
	CColorImageAlpha1Doc* pDoc = GetDocument();
	ASSERT_VALID(pDoc);
	pDoc->OnAddImage();
	Invalidate(TRUE);
}


void CColorImageAlpha1View::OnReverseImage()
{
	// TODO: 여기에 명령 처리기 코드를 추가합니다.
	CColorImageAlpha1Doc* pDoc = GetDocument();
	ASSERT_VALID(pDoc);
	pDoc->OnReverseImage();
	Invalidate(TRUE);
}


void CColorImageAlpha1View::OnBwImage()
{
	// TODO: 여기에 명령 처리기 코드를 추가합니다.
	CColorImageAlpha1Doc* pDoc = GetDocument();
	ASSERT_VALID(pDoc);
	pDoc->OnBwImage();
	Invalidate(TRUE);
}


void CColorImageAlpha1View::OnRgbBw()
{
	// TODO: 여기에 명령 처리기 코드를 추가합니다.
	CColorImageAlpha1Doc* pDoc = GetDocument();
	ASSERT_VALID(pDoc);
	pDoc->OnRgbBw();
	Invalidate(TRUE);
}


void CColorImageAlpha1View::OnGammaImage()
{
	// TODO: 여기에 명령 처리기 코드를 추가합니다.
	CColorImageAlpha1Doc* pDoc = GetDocument();
	ASSERT_VALID(pDoc);
	pDoc->OnGammaImage();
	Invalidate(TRUE);
}


void CColorImageAlpha1View::OnChangeSatur()
{
	// TODO: 여기에 명령 처리기 코드를 추가합니다.
	CColorImageAlpha1Doc* pDoc = GetDocument();
	ASSERT_VALID(pDoc);
	pDoc->OnChangeSatur();
	Invalidate(TRUE);
}


void CColorImageAlpha1View::OnPickOrange()
{
	// TODO: 여기에 명령 처리기 코드를 추가합니다.
	CColorImageAlpha1Doc* pDoc = GetDocument();
	ASSERT_VALID(pDoc);
	pDoc->OnPickOrange();
	Invalidate(TRUE);
}
