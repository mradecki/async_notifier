"""initial_migration

Revision ID: 38a52c38ae81
Revises: 
Create Date: 2023-10-07 21:28:15.776011

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "38a52c38ae81"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "example",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###

    # Create the trigger function
    op.execute(
        """
        CREATE OR REPLACE FUNCTION notify_trigger() RETURNS TRIGGER AS $$
        BEGIN
            PERFORM pg_notify('channel', TG_TABLE_NAME || ', ' || NEW.id);
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
    """
    )

    # Create the trigger
    op.execute(
        """
        CREATE TRIGGER example_update_notify
        AFTER INSERT OR UPDATE OR DELETE ON example
        FOR EACH ROW EXECUTE FUNCTION notify_trigger();
    """
    )



def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("example")
    # ### end Alembic commands ###

    # Drop the trigger
    op.execute("DROP TRIGGER IF EXISTS example_update_notify ON example;")

    # Drop the trigger function
    op.execute("DROP FUNCTION IF EXISTS notify_trigger();")

