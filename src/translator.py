from transformers import MarianMTModel, MarianTokenizer


class 翻译器:
    def __init__(self) -> None:
        self.模型: dict = {}
        self.分词器: dict = {}
        self.语言代码: dict = {
            "zh": "zh",
            "en": "en",
            "de": "de",
            "fr": "fr",
            "ru": "ru",
            "ko": "ko",
            "ja": "ja",
        }

    def _获取模型代码(self, 源语言: str, 目标语言: str) -> str:
        return f"Helsinki-NLP/opus-mt-{self.语言代码[源语言]}-{self.语言代码[目标语言]}"

    def _加载模型(self, 源语言: str, 目标语言: str) -> None:
        模型代码 = self._获取模型代码(源语言, 目标语言)

        if 模型代码 not in self.模型:
            self.模型[模型代码] = MarianMTModel.from_pretrained(模型代码)
            self.分词器[模型代码] = MarianTokenizer.from_pretrained(模型代码)

    @staticmethod
    def 翻译(self, 文本: str, 源语言: str, 目标语言: str) -> str:
        try:
            模型代码 = self._获取模型代码(源语言, 目标语言)

            self._加载模型(源语言, 目标语言)

            已分词 = self.分词器[模型代码].encode(文本, return_tensors="pt")
            翻译结果 = self.模型[模型代码].generate(已分词)
            翻译文本 = self.分词器[模型代码].decode(
                翻译结果[0], skip_special_tokens=True
            )

            return 翻译文本
        except Exception as e:
            print(f"翻译错误: {str(e)}")
            return 文本
