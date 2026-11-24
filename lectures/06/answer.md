# 第6回 解答

## 演習

<!-- [tool call] の行は、表示された行をそのまま貼り付けてください。終わらなかった STEP は、空欄のままでかまいません。 -->

- STEP 1 のツールの名前：
- STEP 2 の [tool call]：glossary_search_glossary({'query': '3レベル'})
- STEP 3 の [tool call]：fetch_fetch({'url': 'https://modelcontextprotocol.io/'})
- STEP 4 の [tool call]：aws_aws___search_documentation({'search_phrase': 'Amazon S3 バージョニング 概要'})
aws_aws___search_documentation({'topics': ['general'], 'search_phrase': 'What is S3 Versioning Amazon Simple Storage Service'})
- 気づき・疑問：外部のMCPサーバを利用することで多様なツールがまとめて使用できるようになったため，その有用性を実感することができた。

## 宿題

<!-- 基礎・実装・発展のどれか1つに取り組めば完了です。 -->

- 取り組んだレベル：発展
- やったこと：VSCodeのMCPサーバ設定方法を調査2026/11/24（https://code.visualstudio.com/docs/agent-customization/mcp-servers, https://code.visualstudio.com/docs/agents/reference/mcp-configuration）
- 結果：ファイルにはすべてのプロジェクトに有効なグローバル設定とそのプロジェクトのみで有効なワークスペース設定の２種類が存在

  | 設定 | ファイル名 | 置き場所 |
  |---|---|---|
  | グローバル設定 | mcp-config.json | ~/.copilot/mcp-config.json |
  | ワークスペース設定 | .mcp.json | ワークスペース（プロジェクト）ルート直下 |

    コマンドでの起動には環境ごとに"npx", "cmd", "python"が存在

    リモートMCPサーバがHTTPSで公開されている場合には "my-remote-server": {"url": "https://example.com/mcp"}　のような表記で接続
- 気づき・疑問：演習において確認した設定方法と大きな差はなかった。
