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
