
"use client"
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger
} from "@/components/ui/accordion"

const items = [{"component_type": "accordion", "value": "item-1", "trigger": "Alex", "content": "Famous people named Alex: Alexander the Great (ancient Macedonian king and conqueror), Alex Trebek (longtime host of Jeopardy!), and Alex Rodriguez (American baseball player)."}, {"component_type": "accordion", "value": "item-2", "trigger": "Maria", "content": "Famous people named Maria: Maria Callas (opera singer), Maria Sharapova (tennis champion), and Maria Montessori (Italian physician and educator)."}, {"component_type": "accordion", "value": "item-3", "trigger": "John", "content": "Famous people named John: John Lennon (musician and member of The Beatles), John Steinbeck (American author), and John F. Kennedy (35th U.S. President)."}, {"component_type": "accordion", "value": "item-4", "trigger": "Michael", "content": "Famous people named Michael: Michael Jordan (basketball legend), Michael Jackson (singer and entertainer), and Michael Faraday (scientist)."}, {"component_type": "accordion", "value": "item-5", "trigger": "Emma", "content": "Famous people named Emma: Emma Watson (actress and activist), Emma Stone (Academy Award\u2013winning actress), and Emma Goldman (political activist and writer)."}]

export default function GeneratedComponent() {
  return (
    <Accordion
      type="multiple"
      collapsible="true"
      defaultValue="item-1"
      className="max-w-lg"
    >

      {items.map((item) => (
        <AccordionItem key={item.value} value={item.value}>
          <AccordionTrigger>{item.trigger}</AccordionTrigger>
          <AccordionContent>{item.content}</AccordionContent>
        </AccordionItem>
      ))}

    </Accordion>
  )
}
