import { test, expect, Page } from '@playwright/test';

const TODO_URL = 'https://demo.playwright.dev/todomvc/';

async function addTodo(page: Page, text: string) {
  const input = page.getByPlaceholder('What needs to be done?');
  await input.fill(text);
  await input.press('Enter');
}

test.describe('Aufgabe 2: Kernfunktionen', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(TODO_URL);
  });

  test('Filter-Logik: All, Active, Completed', async ({ page }) => {
    await addTodo(page, 'Todo 1');
    await addTodo(page, 'Todo 2');
    await addTodo(page, 'Todo 3');

    const items = page.getByTestId('todo-item');
    await items.nth(1).getByRole('checkbox').check();

    await page.getByRole('link', { name: 'Active' }).click();
    await expect(items).toHaveCount(2);
    await expect(items).toHaveText(['Todo 1', 'Todo 3']);

    await page.getByRole('link', { name: 'Completed' }).click();
    await expect(items).toHaveCount(1);
    await expect(items).toHaveText(['Todo 2']);

    await page.getByRole('link', { name: 'All' }).click();
    await expect(items).toHaveCount(3);
  });

  test('Todo bearbeiten und Bearbeitung mit Escape abbrechen', async ({ page }) => {
    await addTodo(page, 'Ursprünglicher Text');

    const item = page.getByTestId('todo-item').first();
    const title = item.getByTestId('todo-title');
    const editField = item.getByRole('textbox', { name: 'Edit' });

    // Bearbeiten und mit Enter bestätigen
    await title.dblclick();
    await editField.fill('Geänderter Text');
    await editField.press('Enter');
    await expect(title).toHaveText('Geänderter Text');

    // Erneut bearbeiten, aber mit Escape abbrechen
    await title.dblclick();
    await editField.fill('Verworfener Text');
    await editField.press('Escape');
    await expect(title).toHaveText('Geänderter Text');
    await expect(page.getByText('Verworfener Text')).toHaveCount(0);
  });

  test('Clear completed und Seiten-Reload', async ({ page }) => {
    await addTodo(page, 'Erledigtes Todo');
    await addTodo(page, 'Offenes Todo');

    const items = page.getByTestId('todo-item');
    await items.nth(0).getByRole('checkbox').check();
    await page.getByRole('button', { name: 'Clear completed' }).click();

    await page.reload();

    await expect(items).toHaveCount(1);
    await expect(items).toHaveText(['Offenes Todo']);
    await expect(page.getByText('Erledigtes Todo')).toHaveCount(0);
  });
});
