from jinja2 import Template

SHADCN_CARD_TEMPLATE = Template("""
"use client"


import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"

export default function GeneratedCard() {
  return (
    <Card>
      <CardHeader>
        <CardTitle>{{ title }}</CardTitle>
        <CardDescription>{{ description }}</CardDescription>
      </CardHeader>
      <CardContent>
        <p>{{ content }}</p>
      </CardContent>
      <CardFooter>
        <p>{{ footer }}</p>
      </CardFooter>
    </Card>
  )
}
""")
