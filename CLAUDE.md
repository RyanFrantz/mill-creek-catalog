# Mill Creek Catalog

This project is a website that catalogs the various species I have observed and
identified within and around Mill Creek.

The website will be static, using semantic HTML (no frameworks like React),
vanilla CSS (no frameworks like Tailwind), and vanilla Javascript.

The website will be responsive, supporting any viewport size and it will follow
accessibility criteria like those defined for
[WCAG](https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum.html).

## Styling and Layout

As much as possible our styling and layout will encourage the browser to do
most of the work determining how to display our content. This means we will
favor approaches such as:

- Setting global style defaults and taking advantage of the cascade, defining
  exceptions as needed.
- Not using utility classes.
- Avoiding units like `px` that aren't universally defined across devices.
- Not using width-based media queries. Prefer to use viewport units (`vw`),
  `rem`, `em`, `ex`, and `ch`, as needed.

An examle of defining a global default and defining exceptions is in the case of
setting a measure for all lines of text. We will define a rule that states "the
measure of [a line] should never exceed 60ch". (1) The CSS that enforces this
rule will look like the following:

```css
:root {
  --measure: 60ch;
}

* {
  max-inline-size: var(--measure);
}

html,
body,
div,
header,
nav,
main,
footer {
  max-inline-size: none;
}
```

(1) Lifted from https://every-layout.dev/rudiments/axioms/
