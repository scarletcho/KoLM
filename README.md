# KoLM
한국어 언어모델 제작을 위한 파이썬 기반 한국어 텍스트처리 패키지입니다.  
**본 패키지 및 Tutorial 은 지속적으로 업데이트되고 있습니다.*
</br>

## Key features
#### 1) utils: 한국어 텍스트처리를 위한 기본 도구들
	- 인코딩 변환, 파일 통합, 어절 통계, 텍스트 정규화 등

#### 2) tag: 형태소와 의사형태소 생성
	- 형태소 분석 (KoNLPy 및 Mecab 연동)
	- 형태소 분석 결과로부터 2가지 유형의 의사형태소(pseudo-morpheme) 생성
		- 최소형태소 (모든 형태 경계를 분리해 가장 작게 잘린 단위; micro)
		- 중간형태소 (체언과 조사만을 분리해 중간 크기로 잘린 단위 ; medium)

#### 3) lm & g2p: 언어모델 제작을 위한 발음정보 및 정제텍스트 생성
	- 문자열로부터 발음열 생성(Grapheme-to-Phone; G2P)
	- 언어모델 제작을 위한 파일 생성
		- 정제된 코퍼스 원문(textraw) 생성
		- 발음사전(lexicon.txt) 생성
</br>
</br>

## Requirements
- Python 2.7 or 3
- Required Python packages:  
	- KoNLPy
	
			$ pip install konlpy
		
	- JPype1
	
			$ pip install JPype1
		
	- korean
	
			$ pip install korean
		
	- hanja
	
			$ pip install hanja
	
	- Mecab
	
			$ bash <(curl -s https://raw.githubusercontent.com/konlpy/konlpy/master/scripts/mecab.sh))
	- [Note] The above packages are **automatically installed** as you install KoLM via pip
</br>

## Installation
- The latest version is available in PyPI:  
	
		$ pip install kolm
</br>

## Tutorial
### 1. utils
- Start by importing every methods in **kolm.utils**
	
		>> from kolm.utils import *

- **convertEncoding***(path, encodingSource, encodingDest, flist=[])*

		# mydir 내 모든 텍스트의 인코딩을 UTF-16에서 UTF-8로 변환
		>> convertEncoding('mydir', 'utf-16', 'utf-8')
		
		# mydir 내 특정 파일들(song1.txt, song2.txt, song15.txt)의 인코딩을 UTF-16에서 UTF-8로 변환
		>> convertEncoding('mydir', 'utf-16', 'utf-8', ['song1.txt', 'song2.txt', 'song15.txt'])
		
- **stackFiles***(path, stackFname, flist=[])*

		# mydir 내 모든 텍스트를 한 파일로 모아 mystack.txt 로 저장하기
		>> stackFiles('mydir', 'mystack.txt')

		# mydir 내 특정 파일들(song1.txt, song2.txt, song15.txt)을 한 파일로 모아 mystack.txt 로 저장하기
		>> stackFiles('mydir', 'mystack.txt', ['song1.txt', 'song2.txt', 'song15.txt'])		
		
- **tightenString***(corpus)*

		>> tightenString(corpus)

- **getEojeolList***(sentlist)*

		>> getEojeolList(['짧은 문장을 넣었다', '새해 복', '집에 갔더니 밥이 없네')
		
- **removeHeader***(headeredfname)*

		>> convertEncoding('mydir', 'utf-16', 'utf-8')

- **readfileUTF8***(fname)*

		# UTF-8 인코딩된 특정 파일(song15.txt)을 읽어들이기
		>> readfileUTF8('song15.txt')
		
- **writefile***(body, fname)*

		# mydir 내 모든 텍스트의 인코딩을 UTF-16에서 UTF-8로 변환하기
		>> convertEncoding('mydir', 'utf-16', 'utf-8')

</br>
### 2. normalize
- Start by importing every methods in **kolm.normalize**
	
		>> from kolm.normalize import *

1. Normalization
	- **Knormalize***(in\_fname, out\_fname)*

			# Normalize a textfile
			>> Knormalize(in_fname, out_fname)
	
	- **normalize***(corpus)*

			# Normalize a text list variable in workspace
			>> normalize(corpus)

	- **bySentence***(corpus)*

			>> bySentence(corpus)
			
	- **removeNonHangul***(line)*
	
			>> removeNonHangul(line)

2. Character reading in Korean
	- Alphabets	
		- **readABC***(line)*
		
				>> readABC(line)
		
		- **readAlphabet***(line)*
		
				>> readAlphabet(line)

	- Hanja (Chinese characters)	
		- **readHanja***(line)*
		
				>> readHanja(line)

	- Hangul jamos (i.e. single letters which do not make a syllable)
		- **readHangulLetter***(line)*
		
				>> readHangulLetter('ㅊ을 ㅈ으로 적었다')
				치읓을 지읒으로 적었다

3. Number reading in Korean
	- Numbers
		- **readNumber***(line)*
		
				>> readNumber(line)

</br>
### 3. tag
- Start by importing every methods in **kolm.tag**
	
		>> from kolm.tag import *

- **morph2pseudo***(raw\_sentlist, morph_sentlist, type)*

		>> morph2pseudo(raw_sentlist, morph_sentlist, type)

- **pseudomorph***(rawText, morphText, pseudoType)*

		>> pseudomorph(rawText, morphText, pseudoType)

- **morphTag***(in\_fname, out\_fname)*

		>> morphTag(in_fname, out_fname)


</br>
### 4. lm
- Start by importing every methods in **kolm.lm**
	
		>> from kolm.lm import *

- **writeTextraw***(corpus)*

		>> writeTextraw(corpus)

- **getUniqueWords***(text\_fname)*

		>> getUniqueWords(text_fname)

- **writeLexicon***(text\_fname)*

		>> writeLexicon(text_fname)


### 5. g2p
- Start by importing every methods in **kolm.g2p**
	
		>> from kolm.g2p import *

1. **Main**
	- **runKoG2P***(rulebook, rulebook\_path)*
	
			# Run Korean G2P on a textfile
			>> runKoG2P(rulebook, rulebook_path)
	
	- **runTest***(rulebook, testset)*

			# Run a test on a testset with a specific rulebook
			>> runTest(rulebook, testset)
			
	- **readRules***(pver, rulebook)*

			>> readRules(pver, rulebook)

2. **Auxiliaries**
	- **phone2prono***(phones, rule\_in, rule\_out)*
	
			>> phone2prono(phones, rule_in, rule_out)
	
	- **graph2prono***(graph, rule\_in, rule\_out)*
	
			>> graph2prono(graph, rule_in, rule_out)
			
	- **graph2phone***(graphs)*
	
			>> graph2phone(graphs)
	
	- **isHangul***(charint)*
			
			>> isHangul(charint)















