class AddStatusToDecisions < ActiveRecord::Migration[7.1]
  def change
    add_column :decisions, :status, :string
  end
end
