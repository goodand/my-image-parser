import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";
import sharp from "sharp";
import path from "path";
import fs from "fs";

// シンプルなロガー（stderr出力でJSON通信を妨げない）
const logger = {
  info: (message: string, data?: any) => {
    const timestamp = new Date().toISOString();
    console.error(`[${timestamp}] INFO: ${message}`, data ? JSON.stringify(data, null, 2) : '');
  },
  error: (message: string, error?: any) => {
    const timestamp = new Date().toISOString();
    console.error(`[${timestamp}] ERROR: ${message}`, error ? error.stack || error : '');
  },
  toolStart: (toolName: string, args: any) => {
    const timestamp = new Date().toISOString();
    console.error(`[${timestamp}] TOOL START: ${toolName}`, JSON.stringify(args, null, 2));
  },
  toolEnd: (toolName: string, success: boolean, result?: any) => {
    const timestamp = new Date().toISOString();
    const status = success ? 'SUCCESS' : 'FAILED';
    console.error(`[${timestamp}] TOOL END: ${toolName} - ${status}`, result ? JSON.stringify(result, null, 2) : '');
  }
};

// 引数から画像フォルダのパスを取得
const imageDir = process.argv[2];
if (!imageDir || !fs.existsSync(imageDir)) {
  logger.error("画像フォルダのパスを指定してください");
  process.exit(1);
}

logger.info("Image Editor MCP Server starting", { imageDir });

const server = new McpServer({
  name: "image-edit-sample-mcp",
  version: "1.0.0",
});

// 画像の明るさ調整ツール
server.registerTool(
  "adjust-brightness",
  {
    title: "画像の明るさ調整",
    description: "画像を明るくまたは暗くします（-1.0〜1.0）",
    inputSchema: {
      filename: z.string(),
      brightness: z.number().min(-1).max(1),
    },
  },
  async ({ filename, brightness }) => {
    const toolName = "adjust-brightness";
    logger.toolStart(toolName, { filename, brightness });
    
    try {
      const filePath = path.join(imageDir, filename);
      const outputPath = path.join(imageDir, `brightness_${filename}`);
      
      // ファイル存在チェック
      if (!fs.existsSync(filePath)) {
        throw new Error(`ファイルが見つかりません: ${filePath}`);
      }
      
      await sharp(filePath)
        .modulate({ brightness: 1 + brightness }) // Sharpの基準は1.0がデフォルト
        .toFile(outputPath);
      
      const result = {
        content: [
          {
            type: "text" as const,
            text: `明るさを調整しました: ${outputPath}`,
          },
        ],
      };
      
      logger.toolEnd(toolName, true, { outputPath });
      return result;
    } catch (error) {
      logger.toolEnd(toolName, false);
      logger.error(`${toolName} failed`, error);
      throw error;
    }
  }
);

// 画像のトリミング（アスペクト比保持）
server.registerTool(
  "crop-image",
  {
    title: "画像のトリミング",
    description: "指定サイズで画像を中央からトリミング（アスペクト比保持）",
    inputSchema: {
      filename: z.string(),
      width: z.number(),
      height: z.number(),
    },
  },
  async ({ filename, width, height }) => {
    const toolName = "crop-image";
    logger.toolStart(toolName, { filename, width, height });
    
    try {
      const filePath = path.join(imageDir, filename);
      const outputPath = path.join(imageDir, `cropped_${filename}`);
      
      // ファイル存在チェック
      if (!fs.existsSync(filePath)) {
        throw new Error(`ファイルが見つかりません: ${filePath}`);
      }
      
      await sharp(filePath)
        .resize(width, height, {
          fit: "cover",
          position: "center",
        })
        .toFile(outputPath);
      
      const result = {
        content: [
          {
            type: "text" as const,
            text: `トリミングを実行しました: ${outputPath}`,
          },
        ],
      };
      
      logger.toolEnd(toolName, true, { outputPath });
      return result;
    } catch (error) {
      logger.toolEnd(toolName, false);
      logger.error(`${toolName} failed`, error);
      throw error;
    }
  }
);

// 画像の圧縮（サイズ指定）
server.registerTool(
  "compress-image",
  {
    title: "画像の圧縮",
    description: "JPEG圧縮で画像サイズを小さくします",
    inputSchema: {
      filename: z.string(),
      quality: z.number().min(1).max(100),
    },
  },
  async ({ filename, quality }) => {
    const toolName = "compress-image";
    logger.toolStart(toolName, { filename, quality });
    
    try {
      const filePath = path.join(imageDir, filename);
      const outputPath = path.join(imageDir, `compressed_${filename}`);
      
      // ファイル存在チェック
      if (!fs.existsSync(filePath)) {
        throw new Error(`ファイルが見つかりません: ${filePath}`);
      }
      
      await sharp(filePath)
        .jpeg({ quality })
        .toFile(outputPath);
      
      const result = {
        content: [
          {
            type: "text" as const,
            text: `圧縮を実行しました: ${outputPath}`,
          },
        ],
      };
      
      logger.toolEnd(toolName, true, { outputPath });
      return result;
    } catch (error) {
      logger.toolEnd(toolName, false);
      logger.error(`${toolName} failed`, error);
      throw error;
    }
  }
);

const transport = new StdioServerTransport();
logger.info("Server connecting to transport");
await server.connect(transport);
logger.info("Image Editor MCP Server ready and waiting for connections");