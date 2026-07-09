# Falconer formatting

Falconer documents use Markdown plus Falconer-specific references and rich blocks.

## References

Preserve existing Falconer references exactly:

```markdown
![f>][reference-id]
![f>][display text][reference-id]
```

Do not invent new reference IDs. If a reference is needed and no ID exists, write normal text and ask the user or use available Falconer tools to find the referenced content.

## Headings

Falconer supports four heading levels:

```markdown
# Heading 1
## Heading 2
### Heading 3
#### Heading 4
```

## Text styles

Use standard Markdown for bold, italic, strikethrough, links, and inline code:

```markdown
**bold**
*italic*
~~struck through~~
`inline code`
[link](https://falconer.com)
```

Highlights use `mark` tags with Falconer color tokens:

```html
<mark data-color="blue" style="background-color: hsl(var(--editor-color-blue)); color: inherit; padding-top: 2px; padding-bottom: 3px;">highlighted text</mark>
```

Supported highlight colors are red, orange, yellow, green, blue, and purple.

## Lists and tasks

Use GitHub-flavored Markdown for lists and task lists:

```markdown
- Parent item
  - Child item

1. First item
2. Second item

- [x] Finished task
- [ ] Open task
```

## Code

Use fenced code blocks with a language:

```python
def greet(name: str) -> str:
    return f"Hello, {name}!"
```

## Tables

Use GitHub-flavored Markdown tables:

```markdown
| Element | How to insert it | Sortable |
| --- | --- | --- |
| Heading | `## ` | No |
| Table | `/table` | Yes |
```

## Math

Falconer renders LaTeX with KaTeX:

```markdown
Inline math: $E = mc^2$

Centered block:

$$
\int_0^\infty e^{-x}\,dx = 1
$$
```

Some existing documents may use `$$inline math$$` or block math fenced with `$$...$$` or `$$$...$$$`. Preserve existing math delimiters unless changing them is necessary.

## Diagrams

Use Mermaid code blocks for diagrams:

```mermaid
flowchart LR
    Write[Write] --> Connect[Connect tools]
    Connect --> Automate[Docs stay current]
```

## Falconer rich components

Falconer documents support rich components beyond standard Markdown. Use them when they make a document clearer or more scannable, but don't force them where plain prose works better. Write them with the exact syntax below - they are parsed from the Markdown you emit.

### Callouts

Highlight a note, warning, or critical message. Use GitHub alert syntax. Supported types: `NOTE`, `CAUTION`, `DANGER`.

```markdown
> [!NOTE]
> Useful context the reader should not miss.

> [!CAUTION]
> Something to be careful about.

> [!DANGER]
> A critical warning.
```

### Accordions

Collapsible sections, good for FAQs or optional detail. Wrap multiple accordions in an `<AccordionGroup>`; a single one can stand alone.

```markdown
<AccordionGroup>
<Accordion title="First question">
Answer content in markdown.
</Accordion>
<Accordion title="Second question">
More content.
</Accordion>
</AccordionGroup>
```

### Tabs

Switch between alternative views of related content. Each tab needs a `title`. For grouped code samples, add `data-code-group="true"` to `<Tabs>`.

```markdown
<Tabs>
<Tab title="Overview">
Content for the first tab.
</Tab>
<Tab title="Details">
Content for the second tab.
</Tab>
</Tabs>
```

### Columns

Place content side by side. `cols` is the number of columns (1-12).

```markdown
<Columns cols={2}>
  <Column>
Left column content.
  </Column>
  <Column>
Right column content.
  </Column>
</Columns>
```

### Cards

A styled container, optionally with an icon, link, and call-to-action button. `icon` takes a Tabler icon name; add `horizontal` for a side-by-side layout.

```markdown
<Card icon="rocket" url="https://example.com" cta="Learn more">
Card content in markdown.
</Card>
```

### Steps

Number a sequence of actions, good for tutorials, setup guides, or any ordered procedure. Wrap each step in a `<Step>` with an optional `title`, and wrap the whole sequence in `<Steps>`.

```markdown
<Steps>
<Step title="Install dependencies">

Run the install command and wait for it to finish.

</Step>
<Step title="Configure the project">

Add your settings to the config file.

</Step>
</Steps>
```

All custom components can contain normal markdown block content (paragraphs, lists, code blocks, etc.).

## Styled text and HTML

For finer visual control, Falconer supports a small set of HTML tags carrying Tailwind utility classes. Use these sparingly - plain markdown is the default, and styling should only be added when it genuinely improves the document.

### Styled headings and paragraphs

To style a heading or paragraph, write it as an HTML tag with a `class` attribute holding Tailwind utility classes. The content between the tags is normal inline markdown.

```markdown
<h2 class="text-center text-blue-600">A centered, colored heading</h2>

<p class="text-sm text-gray-500">A small, muted note.</p>
```

To make a heading render larger or smaller, rewrite it with a `text-*` size class - e.g. a big title as `<h1 class="text-5xl">Title</h1>`.

Limit the classes to these categories: colors (`text-blue-600`), margin (`mt-4`), padding (`px-4`), alignment (`text-center`), font size (`text-sm` through `text-9xl`), font styles (`font-bold`, `italic`, `tracking-wide`), font family (`font-sans`, `font-serif`, `font-mono`), background color (`bg-blue-100`), background gradient (`bg-gradient-to-r`), border (`border-2 border-blue-500`), border radius (`rounded-md`, `rounded-full`), box shadow (`shadow-md`), and text shadow (`text-shadow-md`). Do not use width/height, positioning, or layout utilities.

### Styled images

To style an image - rounding, borders, shadows, margins - write it as an HTML `<img>` tag with a `class` attribute instead of markdown image syntax. Use the same class categories as above.

```markdown
<img src="https://example.com/photo.png" alt="A photo" class="rounded-full shadow-lg border-2 border-gray-200">
```

### Section containers

To give a background, padding, border, or rounded corners to a whole run of content, wrap it in a `<Div>` with a `class` attribute. Leave a blank line after the opening tag and before the closing tag so the inner content is parsed as normal markdown. Always emit the complete `<Div>...</Div>` in a single edit - an unclosed tag breaks the document.

```markdown
<Div class="bg-blue-100 p-4 rounded-md">

## A highlighted section

Normal markdown content goes here and inherits the section's background.

</Div>
```

### Styled inline text

To style only part of a paragraph or heading, wrap that span in a `<Span>` tag with a `class` attribute. Unlike a styled heading or paragraph, `<Span>` is inline and applies to just the wrapped text.

```markdown
This sentence has a <Span class="text-red-600 font-bold">colored, bold phrase</Span> in the middle.
```

### Raw HTML embeds

For an interactive visualization, chart, or animation that the other components cannot express, emit an `<Html>` block. It renders in a sandboxed iframe, so its markup, styles, and scripts are isolated from the document. The whole self-contained document goes between the tags, and the optional `class` attribute sizes the iframe (e.g. `w-full h-96`). Always emit the complete `<Html>...</Html>` block, including the closing tag, in a single edit. Never write or alter `id` attributes - new embeds get one automatically.

```markdown
<Html class="w-full h-96">
<!doctype html>
<html>
  <body>
    <canvas id="c"></canvas>
    <script>/* draw something */</script>
  </body>
</html>
</Html>
```

## Media

For local images or videos, call `upload_media` first and insert the returned snippet. Do not guess asset URLs or write local filesystem paths into Falconer documents.

## Divider

Use a horizontal rule for dividers:

```markdown
---
```
