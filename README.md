# KoLM  
한국어 언어모델 제작을 위한 파이썬 기반 한국어 텍스트처리 패키지입니다.
  
## Key features  
#### 1) utils: 한국어 텍스트처리를 위한 기본 도구들  
	- 파일 관리  
		- 손쉬운 텍스트파일 읽기와 쓰기, 파일 통합  
	- 인코딩 변환  
	- 텍스트 처리  
		- 잉여적인 공백 정리  
		- TEI 헤더 제거  
		- 문장별 어절 목록 정리  
#### 2) normalize: 텍스트 정규화  
	- 텍스트 정규화  
	- 길게 이어진 코퍼스를 문장 단위로 자르기  
	- 한글이 아닌 문자 삭제  
	- 한국어로 된 줄글 외의 문자들 전사  
		- 한글 자모, 한자, 숫자, 알파벳, 영단어 읽기  
  
#### 3) tag: 형태소와 의사형태소 생성  
	- 형태소 분석 (KoNLPy 및 Mecab 연동)  
	- 형태소 분석 결과로부터 2가지 유형의 의사형태소(pseudo-morpheme) 생성  
		- 최소형태소 (모든 형태 경계를 분리해 가장 작게 잘린 단위; micro)  
		- 중간형태소 (체언과 조사만을 분리해 중간 크기로 잘린 단위 ; medium)  
		
		NB. 의사형태소 생성을 위해서는 형태소 분석이 완료된 텍스트가 필요합니다.
		    본 코드는 울산대 UTagger 형태소분석 아웃풋을 전제하여 의사형태소를 생성하기에,
		    입력되는 텍스트 파일이 UTagger 아웃풋과 다를 경우 추가적인 코드 수정 작업이 필요합니다.
  
#### 4) lm & g2p: 언어모델 제작을 위한 발음정보 및 정제텍스트 생성  
	- 문자열로부터 발음열 생성(Grapheme-to-Phone; G2P)  
	- 언어모델 제작을 위한 파일 생성  
		- 정제된 코퍼스 원문(textraw) 생성  
		- 발음사전(lexicon.txt) 생성  
</br>  
</br>  
  
## Requirements  
- Python 2.7 or 3  
- Required Python packages:  
	- KoNLPy, JPype1, korean, hanja, Mecab  
	- [Note] The above packages are **automatically installed** as you install KoLM via pip  
</br>  
</br>  
  
## Installation  
- The latest version is available in PyPI:    
	  
		$ pip install kolm  
</br>  
  
## Tutorial: How to use KoLM  
* 말뭉치 정제 작업 가이드:  
	* (1) 모든 텍스트를 UTF-8로 인코딩 변환  
		* utils.**convertEncoding**  
	* (2) 모든 텍스트를 하나로 이어붙여 저장하기  
		* utils.**stackFiles**  
	* (3) TEI 헤더 (또는 분석대상이 아닌 태그류) 제거  
		* utils.**removeHeader**  
	* (4) 텍스트 정규화  
		* normalize.**Knormalize**  
	* (5) 형태소분석  
		* tag.**morphTag**  
	* (6) 원문-형태소 대조를 통한 의사형태소 추출  
		* tag.**pseudomorph**  
	* (7) 정제텍스트(textraw)와 발음사전(lexicon.txt) 생성  
		* lm.**writeTextraw**  
		* lm.**getUniqueWords**  
		* lm.**writeLexicon**  
  
* 구체적인 사용 예시 코드를 보려면 **runKoLM.py** 를 참조하세요.  
  
## 1. utils  
- Start by importing every method in **kolm.utils**  
	  
		>> from kolm.utils import *  
  
  
1. **File management**  
	- **readfileUTF8** *(fname)*  
	  
			# UTF-8 인코딩된 특정 파일(song15.txt)을 읽어들이기  
			>> readfileUTF8('song15.txt')  
			  
	- **writefile** *(body, fname)*  
	  
			# mydir 내 모든 텍스트의 인코딩을 UTF-16에서 UTF-8로 변환하기  
			>> convertEncoding('mydir', 'utf-16', 'utf-8')  
			  
	- **stackFiles** *(path, stackFname, flist=[])*  
	  
			# mydir 내 모든 텍스트를 한 파일로 모아 mystack.txt 로 저장하기  
			>> stackFiles('mydir', 'mystack.txt')  
	  
			# mydir 내 특정 파일들(song1.txt, song2.txt, song15.txt)을 한 파일로 모아 mystack.txt 로 저장하기  
			>> stackFiles('mydir', 'mystack.txt', ['song1.txt', 'song2.txt', 'song15.txt'])		  
</br>  
  
2. **Encoding**    
	- **convertEncoding** *(path, encodingSource, encodingDest, flist=[])*    
	  
			# mydir 내 모든 텍스트의 인코딩을 UTF-16에서 UTF-8로 변환  
			>> convertEncoding('mydir', 'utf-16', 'utf-8')  
			  
			# mydir 내 특정 파일들(song1.txt, song2.txt, song15.txt)의 인코딩을 UTF-16에서 UTF-8로 변환  
			>> convertEncoding('mydir', 'utf-16', 'utf-8', ['song1.txt', 'song2.txt', 'song15.txt'])  
</br>  
  
3. **Text management**    
	- **tightenString** *(corpus)*    
  
			# 텍스트 리스트 내 잉여적인 공백 정리 및 삭제  
			>> tightenString(corpus)  
	  
	- **getEojeolList** *(sentlist)*    
			  
			# 문장 리스트에서 어절 리스트 추출  
			>> getEojeolList(['짧은 문장을 넣었다', '새해 복', '집에 갔더니 밥이 없네')  
			  
	- **removeHeader** *(headeredfname)*  
	  
			>> convertEncoding('mydir', 'utf-16', 'utf-8')  
	  

</br>  
  
## 2. normalize  
- Start by importing every method in **kolm.normalize**  
	  
		>> from kolm.normalize import *  
  
1. **Normalization**  
	- **Knormalize** *(in\_fname, out\_fname)*  
  
			# Normalize a textfile  
			>> Knormalize(in_fname, out_fname)  
	  
	- **normalize** *(corpus)*  
  
			# Normalize a text list variable in workspace  
			>> normalize(corpus)  
  
	- **bySentence** *(corpus)*  
  
			>> bySentence(corpus)  

	- **removeNonHangul** *(line)*  
  
			>> removeNonHangul(line)  

</br>  
  
2. **Character reading in Korean**  
	- Alphabets	  
		- **readABC** *(line)*  
		  
				>> readABC(line)  
		  
		- **readAlphabet** *(line)*  
		  
				>> readAlphabet(line)  
  
	- Hanja (Chinese characters)	  
		- **readHanja** *(line)*  
		  
				>> readHanja(line)  
  
	- Hangul jamos (i.e. single letters which do not make a syllable)  
		- **readHangulLetter** *(line)*  
		  
				>> readHangulLetter('ㅊ을 ㅈ으로 적었다')  
				치읓을 지읒으로 적었다  

</br>  
  
3. **Number reading in Korean**  
	- **readNumber** *(line)*  
	  
			>> readNumber(line)  
  
</br>  
  
## 3. tag  
- Start by importing every method in **kolm.tag**  
	  
		>> from kolm.tag import *  
		  
1. **Morphemes**  
	- **morphTag** *(in\_fname, out\_fname)*  
	  
			# Mecab 형태소분석  
			>> morphTag(in_fname, out_fname)  

</br>  
  
2. **Pseudo-morphemes**    
	- **morph2pseudo** *(raw\_sentlist, morph_sentlist, type)*  
  
			# 문장 리스트로부터 의사형태소(최소 크기) 문장 리스트 생성  
			>> morph2pseudo(raw_sentlist, morph_sentlist, 'micro')  
	  
			# 문장 리스트로부터 의사형태소(중간 크기) 문장 리스트 생성  
			>> morph2pseudo(raw_sentlist, morph_sentlist, 'medium')  
			  
	- **pseudomorph** *(rawText, morphText, pseudoType)*  
		  
			# 문장 하나로부터 의사형태소(최소 크기) 문장 생성  
			>> pseudomorph(rawText, morphText, 'micro')  
  
			# 문장 하나로부터 의사형태소(중간 크기) 문장 생성  
			>> pseudomorph(rawText, morphText, 'medium')  
  
</br>  
  
## 4. lm  
- Start by importing every method in **kolm.lm**  
	  
		>> from kolm.lm import *  
  
- **writeTextraw** *(corpus)*  
		  
		# 정제를 마친 단일 말뭉치 파일(textraw) 생성  
		>> writeTextraw(corpus)  
  
- **getUniqueWords** *(text\_fname)*  
  
		# 고유 어절(또는 형태소; 말뭉치 상의 띄어쓰기된 단위를 의미)목록(wordlist.txt) 추출  
		>> getUniqueWords(text_fname)  
  
- **writeLexicon** *(text\_fname)*  
		  
		# 고유 어절목록에 G2P를 적용한 발음사전(lexicon.txt) 생성  
		>> writeLexicon(text_fname)  
</br>  
  
## 5. g2p  
- Start by importing every method in **kolm.g2p**  
	  
		>> from kolm.g2p import *  
  
1. **Main**  
	- **runKoG2P** *(hangeul_sequence, rulebook\_path)*  
	  
			# Run Korean G2P on a sequence  
			>> runKoG2P(hangeul_sequence, rulebook_path)  
	  
	- **runTest** *(rulebook, testset)*  
  
			# Run a test on a testset with a specific rulebook  
			>> runTest(rulebook, testset)  
	
	- **readRules** *(pver, rulebook)*  
  
			>> readRules(pver, rulebook)  

</br>  
  
2. **Auxiliaries**  
	- **phone2prono** *(phones, rule\_in, rule\_out)*  
	  
			>> phone2prono(phones, rule_in, rule_out)  
	  
	- **graph2prono** *(graph, rule\_in, rule\_out)*  
	  
			>> graph2prono(graph, rule_in, rule_out)  
			  
	- **graph2phone** *(graphs)*  
	  
			>> graph2phone(graphs)  
	  
	- **isHangul** *(charint)*  
			  
			>> isHangul(charint)  
  
  
  
