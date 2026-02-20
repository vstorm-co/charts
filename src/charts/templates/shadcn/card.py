"""Jinja2 template for generating shadcn/ui Card components.

Renders a structured card with header (title/description), body content,
and footer sections using standard shadcn/ui Card primitives.

Template variables:
    title: Card title displayed in CardHeader
    description: Subtitle or description text
    content: Main content (text or React component)
    footer: Footer text displayed at bottom

Example:
    ```python
    template = SHADCN_CARD_TEMPLATE.render(
        title="Statistics",
        description="Monthly metrics overview",
        content="Total visitors: 12,345",
        footer="Last updated today"
    )
    ```
"""

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
