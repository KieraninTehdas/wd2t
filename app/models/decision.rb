# frozen_string_literal: true

class Decision < ApplicationRecord
  belongs_to :creator, class_name: "User", default: -> { Current.user }

  validates :title, presence: true

  enum :status, {
    pending: "pending",
    accepted: "accepted",
    rejected: "rejected",
    superceded: "superceded"
  }
end
