"""Jinja2 template for generating shadcn/ui Accordion components.

Renders collapsible content panels supporting both single and multiple
expansion modes via the type attribute.

Template variables:
    items_json: JSON string of accordion item data (value, trigger, content)
    list_type: Expansion mode - "single" or "multiple"
    items: List of AccordionItem objects for defaultValue

Example:
    ```python
    template = SHADCN_ACCORDION_TEMPLATE.render(
        items_json='[{"value": "1", "trigger": "Title", "content": "Text"}]',
        list_type="single"
    )
    ```
"""

from jinja2 import Template

SHADCN_ACCORDION_TEMPLATE = Template("""
"use client"
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger
} from "@/components/ui/accordion"

const items = {{ items_json }}

export default function GeneratedComponent() {
  return (
    <Accordion
      type="{{ list_type }}"
      collapsible="true"
      defaultValue="{{ items[0].value if items else '' }}"
      className="max-w-lg"
    >
      {% raw %}
      {items.map((item) => (
        <AccordionItem key={item.value} value={item.value}>
          <AccordionTrigger>{item.trigger}</AccordionTrigger>
          <AccordionContent>{item.content}</AccordionContent>
        </AccordionItem>
      ))}
      {% endraw %}
    </Accordion>
  )
}
""")
