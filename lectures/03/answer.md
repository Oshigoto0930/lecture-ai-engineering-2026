# 第3回 解答

## 演習

- 第1回（素のLLM）とエージェントの回答の違い：glossary.jsonの内容と会っており，関係する回として第１回が示された。
- `--trace` で見えたツール呼び出し（ツール名と引数）：ツール名search_glossary，引数{'query': 'LoRA'}{'query': 'QLoRA'}
- 1つの質問での LLM 呼び出し回数（`requests`）：requests=2
- 追加したツールと、docstring に書いた説明：[make_quiz]
  指定した回の用語から 1つを選び、
  確認問題と答えを返す。
  「第2回の確認問題を出して」のように、
  復習用の問題を求められたときに使う。
  引数: {"lecture": {"type": "integer"}}

## 宿題

- 取り組んだレベル：実装
- やったこと：tools.pyにおいて保存先にlearning_log/を定義，save_learning_logを追加。agent.pyにDeferredToolResultsをインポート，output_typeへDeferredToolRequests追加，save_learning_logを承認必須で登録
- 結果：操作者への確認を経てlearning_logに指示した内容が保存されているのを確認。
- 気づき・疑問：ツールの実装方法や，それをエージェントに使用させるためのハーネスの設定しついて学ぶことができた。このようなシンプルな機能を実装するだけでも，これだけの箇所に加筆をする必要があることに驚いた。
