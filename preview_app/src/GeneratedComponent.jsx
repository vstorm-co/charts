
"use client"
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger} from "@/components/ui/accordion"

const items = [{"component_type": "accordion", "value": "prime-2", "trigger": "2", "content": "2 is the only even prime number. Every other even number can be divided by 2, so 2 is uniquely \u2018odd\u2019 among the evens."}, {"component_type": "accordion", "value": "prime-3", "trigger": "3", "content": "3 is the first odd prime and shows up everywhere in jokes and stories\u2014think \u2018the rule of three\u2019 in comedy and writing."}, {"component_type": "accordion", "value": "prime-5", "trigger": "5", "content": "5 is the number of fingers on a hand, which might be why we love counting money and high\u2011fiving with this prime."}, {"component_type": "accordion", "value": "prime-7", "trigger": "7", "content": "7 is often called a \u2018magic\u2019 or \u2018lucky\u2019 number. There are 7 days in a week, 7 continents, and 7 is suspiciously overused in trivia questions."}, {"component_type": "accordion", "value": "prime-11", "trigger": "11", "content": "11 is the first two-digit prime and also looks like two fence posts standing next to each other, guarding the entrance to bigger primes."}, {"component_type": "accordion", "value": "prime-13", "trigger": "13", "content": "13 has a spooky reputation in superstition, but mathematically it\u2019s just an innocent prime number minding its own business."}, {"component_type": "accordion", "value": "prime-17", "trigger": "17", "content": "17 is sometimes called a \u2018random\u2011looking\u2019 number. In informal polls, people asked to pick a random number from 1\u201320 choose 17 more than any other."}]

export default function GeneratedComponent() {
  return (
    <Accordion
      type="multiple"
      collapsible="true"
      defaultValue="prime-2"
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
