# Jinja2 Templates

The library uses Jinja2 templates for rendering components.

## Template Files

Located in [`src/charts/templates/shadcn/`](https://github.com/vstorm-co/charts/tree/main/src/charts/templates/shadcn):

| File | Purpose |
| ------ | --------- |
| `table.py` | Table with headers, rows, footer |
| `chart.py` | Bar, Line, Pie, Area, Radar charts |
| `accordion.py` | Collapsible accordion panels |
| `card.py` | Card container with sections |
| `carousel.py` | Horizontal/vertical carousel |

## Template Variables

### Common Variables

| Variable | Type | Description |
| ---------- | ------ | ------------- |
| `title` | str | Component title |
| `description` | str | Component description |

### Table Template Variables

| Variable | Type | Description |
| ---------- | ------ | ------------- |
| `items_json` | str | JSON array of row data |
| `headers` | list[str] | Column headers |
| `caption` | str | Table caption |
| `footer_text` | str | Footer keyword (e.g., "Total") |
| `footer_value` | int \| float \| None | Calculated footer value |

### Chart Template Variables

| Variable | Type | Description |
| ---------- | ------ | ------------- |
| `chart_config_json` | str | JSON config mapping keys to labels/colors |
| `chart_data_json` | str | JSON array of data points |
| `title` | str | Chart title |
| `description` | str | Chart description |
| `x_axis_key` | str | Key for x-axis labels |
| `value_key` | str | Key for Y values (pie chart specific) |
| `data_keys` | list[str] | List of data series keys |

### Accordion Template Variables

| Variable | Type | Description |
| ---------- | ------ | ------------- |
| `items_json` | str | JSON array of accordion items |
| `list_type` | str | "single" or "multiple" |

### Carousel Template Variables

| Variable | Type | Description |
| ---------- | ------ | ------------- |
| `items_json` | str | JSON array of carousel items |
| `align` | str \| None | Alignment setting |
| `loop` | str \| None | Loop mode ("true"/"false") |
| `orientation` | str | "horizontal" or "vertical" |
| `container_class` | str \| None | CSS class for container |

## Example Template

```python
from jinja2 import Template

TABLE_TEMPLATE = Template("""
<div class="w-full">
  <caption class="text-sm font-medium text-foreground mb-4">{{ caption }}</caption>
  <div class="rounded-md border">
    <table class="w-full caption-bottom text-sm">
      <thead class="[&_tr]:border-b">
        <tr class="border-b transition-colors hover:bg-muted/50 data-[state=selected]:bg-muted">
          {% for header in headers %}
            <th class="h-12 px-4 text-left align-middle font-medium text-muted-foreground">
              {{ header }}
            </th>
          {% endfor %}
        </tr>
      </thead>
      <tbody class="[&_tr:last-child]:border-0">
        {% for row in items_json %}
          <tr class="border-b transition-colors hover:bg-muted/50">
            {% for key, value in row.items() %}
              <td class="p-4 align-middle">{{ value }}</td>
            {% endfor %}
          </tr>
        {% endfor %}
      </tbody>
      {% if footer_value %}
        <tfoot class="border-t bg-gray-50/50 dark:bg-gray-900/50">
          <tr>
            <td colspan="{{ headers|length }}" class="h-12 px-4 text-left">
              {{ footer_text }}: {{ footer_value }}
            </td>
          </tr>
        </tfoot>
      {% endif %}
    </table>
  </div>
</div>
""")
```

## Template Rendering

```python
from jinja2 import Template

template = Template("Hello {{ name }}")
output = template.render(name="World")
# Output: "Hello World"
```
