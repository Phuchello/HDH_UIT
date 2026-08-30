import { QuartzConfig } from "./quartz/cfg"
import * as Plugin from "./quartz/plugins"

/**
 * Quartz 4.0 Configuration for HDH_UIT V2
 * IT007 — Cẩm Nang & Vườn Tri Thức Hệ Điều Hành UIT
 */
const config: QuartzConfig = {
  configuration: {
    pageTitle: "IT007 · Hệ Điều Hành",
    pageTitleSuffix: " — IT007 UIT",
    enableSPA: true,
    enablePopovers: true,
    analytics: null,
    locale: "vi-VN",
    baseUrl: "phuchello.github.io/HDH_UIT",
    ignorePatterns: ["private", "templates", ".obsidian"],
    defaultDateType: "created",
    theme: {
      fontOrigin: "local",
      cdnCaching: false,
      typography: {
        header: "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
        body: "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
        code: "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace",
      },
      colors: {
        lightMode: {
          light: "#fbfbf9",
          lightgray: "#f4f4f0",
          gray: "#e2e2da",
          darkgray: "#57606a",
          dark: "#1f2328",
          secondary: "#0969da",
          tertiary: "#0e7490",
          highlight: "#ddf4ff",
          textHighlight: "#0969da88",
        },
        darkMode: {
          light: "#0d1117",
          lightgray: "#161b22",
          gray: "#30363d",
          darkgray: "#8b949e",
          dark: "#e6edf3",
          secondary: "#58a6ff",
          tertiary: "#38bdf8",
          highlight: "rgba(56, 139, 253, 0.15)",
          textHighlight: "#58a6ff88",
        },
      },
    },
  },
  plugins: {
    transformers: [
      Plugin.FrontMatter(),
      Plugin.CreatedModifiedDate({
        priority: ["frontmatter", "filesystem"],
      }),
      Plugin.SyntaxHighlighting({
        theme: {
          light: "github-light",
          dark: "github-dark",
        },
        keepBackground: false,
      }),
      Plugin.ObsidianFlavoredMarkdown({ enableInHtmlEmbed: false }),
      Plugin.GitHubFlavoredMarkdown(),
      Plugin.TableOfContents(),
      Plugin.CrawlLinks({ markdownLinkResolution: "shortest" }),
      Plugin.Description(),
      Plugin.Latex({ renderEngine: "katex" }),
    ],
    filters: [Plugin.RemoveDrafts()],
    emitters: [
      Plugin.AliasRedirects(),
      Plugin.ComponentResources(),
      Plugin.ContentPage(),
      Plugin.FolderPage(),
      Plugin.TagPage(),
      Plugin.ContentIndex({
        enableSiteMap: true,
        enableRSS: false,
      }),
      Plugin.Assets(),
      Plugin.Static(),
      Plugin.NotFoundPage(),
    ],
  },
}

export default config
