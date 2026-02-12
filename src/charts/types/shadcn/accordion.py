from charts.base_types import BaseAccordion, BaseAccordionItem


class AccordionItem(BaseAccordionItem):
    """Accordion element to be rendered on the frontend.

    Example:
    {
        value: "item-1",
        trigger: "How do I reset my password?",
        content: "Click on 'Forgot Password' on the login page, enter
        your email address, and we'll send you a link to reset your
        password. The link will expire in 24 hours."
    }

    """

    component_type: str = "accordion_item"


class Accordion(BaseAccordion):
    """A list-type collection of Accordion objects for rendering purposes.

    Example:
    { items: [
        { value: "item-1",
        trigger: "How do I reset my password?",
        content: "Click on 'Forgot Password' on the login page, enter your
            email address, and we'll send you a link to reset your password.
            The link will expire in 24 hours."
        },
        { value: "item-2",
        trigger: "Can I change my subscription plan?",
        content: "Yes, you can upgrade or downgrade your plan at any time
        from your account settings. Changes will be reflected in your
        next billing cycle."
        }],
    list_type: "multiple"
    }

    """

    component_type: str = "accordion"
