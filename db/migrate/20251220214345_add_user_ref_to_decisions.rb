class AddUserRefToDecisions < ActiveRecord::Migration[8.1]
  def change
    add_reference :decisions, :creator, null: false, foreign_key: { to_table: :users }
  end
end
