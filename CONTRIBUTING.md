# 🤝 기여 가이드 | Contributing Guide

neo-says에 기여해 주셔서 감사합니다! 이 문서는 프로젝트에 기여하는 방법을 안내합니다.

Thank you for contributing to neo-says! This guide explains how to contribute.

## 명언 추가하기 | Adding Quotes

### 방법 1: 이슈로 제출 (비개발자 추천)

1. [Quote Submission](../../issues/new?template=quote-submission.yml) 이슈를 생성합니다
2. 양식을 작성합니다
3. 메인테이너가 검토 후 추가합니다

### 방법 2: PR로 직접 추가 (개발자 추천)

1. 리포를 Fork합니다
2. 브랜치를 생성합니다: `git checkout -b add-quote-author-name`
3. `data/quotes.json`에 명언을 추가합니다:

```json
{
  "text": "Your quote here.",
  "author": "Author Name",
  "category": "motivation"
}
```

4. JSON 형식이 유효한지 확인합니다: `npm test` 또는 `python -m json.tool data/quotes.json`
5. 커밋합니다: `git commit -m "feat: add quote by Author Name"`
6. PR을 생성합니다

### 명언 규칙

- 중복 금지: 기존 명언과 동일한 내용이 없어야 합니다
- 저자 정확성: 정확한 저자 정보를 기재해 주세요
- 카테고리: `motivation`, `wisdom`, `humor`, `philosophy`, `science`, `life`, `other` 중 선택
- 언어: 영어 명언을 기본으로 합니다 (다른 언어는 원문과 영어 번역 모두 포함)

## 코드 기여 | Code Contributions

### 개발 환경 설정

```bash
# Fork & Clone
git clone https://github.com/YOUR_USERNAME/neo-says.git
cd neo-says

# 의존성 설치 (Node.js)
npm install

# 또는 Python
pip install -e ".[dev]"
```

### 코드 스타일

- **Shell**: ShellCheck 린팅 통과 필수
- **JavaScript**: ESLint + Prettier
- **Python**: Ruff 포매터
- **커밋 메시지**: [Conventional Commits](https://www.conventionalcommits.org/) 형식
  - `feat:` 새 기능
  - `fix:` 버그 수정
  - `docs:` 문서 수정
  - `test:` 테스트
  - `chore:` 기타

### PR 규칙

1. 하나의 PR에는 하나의 변경 사항만 포함합니다
2. PR 템플릿을 빠짐없이 작성합니다
3. CI가 통과해야 머지됩니다
4. 리뷰어의 피드백에 응답해 주세요

## 버그 리포트 | Bug Reports

[Bug Report](../../issues/new?template=bug-report.yml) 이슈 템플릿을 사용해 주세요.

## 질문 & 토론 | Questions & Discussions

[Discussions](../../discussions) 탭에서 자유롭게 질문하거나 아이디어를 공유해 주세요.

## 라이선스 | License

기여하시는 내용은 프로젝트의 MIT 라이선스에 따라 배포됩니다.
