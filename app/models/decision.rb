# frozen_string_literal: true

class Decision < ApplicationRecord
  validates :title, presence: true

  enum status: {
    pending: "pending",
    accepted: "accepted",
    rejected: "rejected",
    superceded: "superceded"
  }
end
