import { test, expect, Page } from '@playwright/test';

const TODO_URL = 'https://demo.playwright.dev/todomvc/';

async function addTodo(page: Page, text: string) {
  const input = page.getByPlaceholder('What needs to be done?');
  await input.fill(text);
  await input.press('Enter');
}

test.describe('Aufgabe 3: Fortgeschrittene Szenarien & Edge-Cases', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(TODO_URL);
  });

  test('Leere Eingaben und reine Leerzeichen werden abgewiesen', async ({ page }) => {
    const input = page.getByPlaceholder('What needs to be done?');

    await input.press('Enter');
    await input.fill('   ');
    await input.press('Enter');

    await expect(page.getByTestId('todo-item')).toHaveCount(0);
    await expect(page.getByTestId('todo-count')).toBeHidden();
    await expect(page.locator('footer.footer')).toBeHidden();
  });

  test('Toggle All markiert alle Todos und synchronisiert den Zähler', async ({ page }) => {
    await addTodo(page, 'Todo 1');
    await addTodo(page, 'Todo 2');
    await addTodo(page, 'Todo 3');

    const toggleAll = page.getByLabel('Mark all as complete');
    const items = page.getByTestId('todo-item');
    const counter = page.getByTestId('todo-count');

    await toggleAll.click();
    await expect(counter).toHaveText('0 items left');
    for (let i = 0; i < 3; i++) {
      await expect(items.nth(i)).toHaveClass(/completed/);
    }

    await toggleAll.click();
    await expect(counter).toHaveText('3 items left');
    for (let i = 0; i < 3; i++) {
      await expect(items.nth(i)).not.toHaveClass(/completed/);
    }
  });

  test('Einzelnes Todo über das Hover-Symbol (×) löschen', async ({ page }) => {
    await addTodo(page, 'Zu löschendes Todo');

    const todoItem = page.getByTestId('todo-item').first();
    await todoItem.hover();
    await todoItem.getByRole('button', { name: 'Delete' }).click();

    await expect(page.getByTestId('todo-item')).toHaveCount(0);
  });

  test('Daten werden korrekt im localStorage gespeichert', async ({ page }) => {
    await addTodo(page, 'Erstes Todo');
    await addTodo(page, 'Zweites Todo');
    await page.getByTestId('todo-item').nth(0).getByRole('checkbox').check();

    const storedData = await page.evaluate(() => localStorage.getItem('react-todos'));
    const todos = JSON.parse(storedData ?? '[]');

    expect(todos).toHaveLength(2);
    expect(todos[0].title).toBe('Erstes Todo');
    expect(todos[0].completed).toBe(true);
    expect(todos[1].title).toBe('Zweites Todo');
    expect(todos[1].completed).toBe(false);
  });
});
