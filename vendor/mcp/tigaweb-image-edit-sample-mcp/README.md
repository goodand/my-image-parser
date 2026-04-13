# Image Editor MCP Server

> **⚠️ 学習用プロジェクト**
> 
> このプロジェクトは**MCP（Model Context Protocol）の学習・理解を目的**として作成されています。
> **実際のプロダクション環境での使用は想定されていません。**

## 概要

このプロジェクトは、Claude DesktopなどのAIクライアントから画像編集機能を利用できるMCPサーバーの学習実装です。

### 提供機能

- **明るさ調整**: 画像の明度を調整（-1.0〜1.0）
- **画像トリミング**: 指定サイズでの中央トリミング（アスペクト比保持）
- **画像圧縮**: JPEG品質指定での圧縮（1-100）

## 技術スタック

- **Node.js** + **TypeScript**
- **MCP SDK** (@modelcontextprotocol/sdk)
- **Sharp** (画像処理ライブラリ)
- **Zod** (スキーマ検証)
- **tsx** (TypeScript実行環境)

## セットアップ

### 1. 依存関係のインストール

```bash
npm install
```

### 2. 画像フォルダの作成

```bash
mkdir images
# テスト用画像を images/ フォルダに配置
```

### 3. サーバーの起動テスト

```bash
npm start ./images
```

## Claude Desktop設定

Claude Desktopで使用する場合は、以下の設定を `~/Library/Application Support/Claude/claude_desktop_config.json` に追加：

```json
{
  "mcpServers": {
    "image-edit-sample-mcp": {
      "command": "/Users/YOUR_USERNAME/.volta/bin/npx",
      "args": [
        "-y",
        "tsx",
        "/path/to/your/image-edit-sample-mcp/src/server.ts",
        "/path/to/your/image-edit-sample-mcp/images"
      ]
    }
  }
}
```

**注意**: パスは実際の環境に合わせて変更してください。

## 使用例

Claude Desktopでの使用例：

```
imagesフォルダのphoto.jpgの明るさを0.3上げてください
```

```
sample.jpgを800x600にトリミングしてください
```

```
large.jpgを品質80で圧縮してください
```

## ファイル構成

```
image-edit-sample-mcp/
├── src/
│   └── server.ts          # MCPサーバーメイン実装
├── images/                # 画像ファイル格納フォルダ
├── package.json
├── tsconfig.json
├── .gitignore
└── README.md
```

## 学習ポイント

このプロジェクトで学べる内容：

### MCP（Model Context Protocol）
- MCPサーバーの基本実装
- ツール登録とスキーマ定義
- JSON-RPC通信の理解
- stdio通信での連携

### TypeScript/Node.js
- ES Modules環境でのTypeScript実行
- Zodを使ったスキーマ検証
- エラーハンドリングとロギング

### 画像処理
- Sharpライブラリの基本操作
- 画像の明度・サイズ・品質調整

## 注意事項

- **学習目的専用**: 本格的な画像編集には適していません
- **エラーハンドリング**: 最小限の実装のため、本番環境では不十分
- **セキュリティ**: ファイルパスの検証などが簡易的
- **パフォーマンス**: 大量処理には対応していません

## ライセンス

ISC

## 参考リンク

- [Model Context Protocol](https://modelcontextprotocol.io/)
- [Sharp (画像処理ライブラリ)](https://sharp.pixelplumbing.com/)
- [Claude Desktop](https://claude.ai/desktop) 