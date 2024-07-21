# frozen_string_literal: true

module DecisionsHelper
  def status_text(status)
    status_classes = {
      pending: "text-white bg-blue-600",
      accepted: "bg-lime-500",
      rejected: "bg-pink-500",
      superceded: "text-white bg-pink-700"
    }
    classes = status_classes.fetch(status.to_sym, "bg-indigo-500")

    content_tag(:p, status.capitalize, class: "rounded shadow-lg px-3 font-medium #{classes}")
  end
end
