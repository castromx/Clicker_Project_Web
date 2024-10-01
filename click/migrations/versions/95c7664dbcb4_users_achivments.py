from alembic import op
import sqlalchemy as sa

# Ідентифікатори ревізії, що використовуються Alembic.
revision = '95c7664dbcb4'
down_revision = '3738cf031c8a'
branch_labels = None
depends_on = None

def upgrade():
    # Крок 1: Додати стовпець з дефолтним значенням
    op.add_column('charge', sa.Column('user', sa.Integer(), server_default='0', nullable=False))

    # Крок 2: Оновити існуючі рядки з відповідними значеннями (за необхідності)
    # Примітка: Змініть цей запит відповідно до ваших реальних вимог і даних
    op.execute('UPDATE charge SET user = 1 WHERE user IS NULL')  # Приклад запиту

    # Крок 3: Змінити стовпець, щоб видалити дефолтне значення
    with op.batch_alter_table('charge') as batch_op:
        batch_op.alter_column('user', server_default=None)

def downgrade():
    # У функції downgrade ви можете скасувати ці кроки
    with op.batch_alter_table('charge') as batch_op:
        batch_op.drop_column('user')
