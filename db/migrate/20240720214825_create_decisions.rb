class CreateDecisions < ActiveRecord::Migration[7.1]
  def change
    create_table :decisions do |t|
      t.string :title
      t.date :date
      t.text :description

      t.timestamps
    end
  end
end
